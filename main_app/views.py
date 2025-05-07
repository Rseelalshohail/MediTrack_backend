from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timesince import timesince
from django.utils.timezone import now
from .permissions import IsAdminUser, IsEngineerUser, IsNurseUser, IsAdminOrEngineer, IsAdminOrNurse
from .models import Hospital, Room, Device, WorkOrder, SparePartRequest, Admin, Engineer, Nurse
from .serializers import (
    HospitalSerializer, RoomSerializer, DeviceReadSerializer, DeviceWriteSerializer,
    WorkOrderReadSerializer, WorkOrderWriteSerializer, SparePartRequestReadSerializer,
    SparePartRequestWriteSerializer, AdminSerializer, EngineerSerializer, NurseSerializer,
    UserSerializer
)

User = get_user_model()

class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Admin created successfully", "username": user.username, "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EngineerSignupView(APIView):
    def post(self, request):
        serializer = EngineerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Engineer created successfully", "username": user.username, "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NurseSignupView(APIView):
    def post(self, request):
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Nurse created successfully", "username": user.username, "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        user_type = 'admin' if hasattr(user, 'admin') else 'engineer' if hasattr(user, 'engineer') else 'nurse' if hasattr(user, 'nurse') else None

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "username": user.username,
            "user_type": user_type,
        })

class Home(APIView):
    def get(self, request):
        return Response({
            "message": "🎉 Welcome to the MediTrack API!",
            "available_endpoints": {
                "hospitals": "/api/hospitals/",
                "rooms": "/api/rooms/",
                "devices": "/api/devices/",
                "work_orders": "/api/workorders/",
                "spare_parts": "/api/spareparts/",
                "signup_admin": "/api/signup/admin/",
                "signup_engineer": "/api/signup/engineer/",
                "signup_nurse": "/api/signup/nurse/",
                "login": "/api/token/",
                "user_list_by_type": "/api/users/?type=engineer"
            },
            "version": "v1.0",
            "status": "API is running ✅"
        })

class HospitalListCreateView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class HospitalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()

    def get_serializer_class(self):
        return DeviceReadSerializer if self.request.method == 'GET' else DeviceWriteSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()

    def get_serializer_class(self):
        return DeviceReadSerializer if self.request.method == 'GET' else DeviceWriteSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  
        return [IsAuthenticated(), IsAdminUser()]  


class WorkOrderListCreateView(generics.ListCreateAPIView):
    queryset = WorkOrder.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrNurse]

    def get_serializer_class(self):
        return WorkOrderReadSerializer if self.request.method == 'GET' else WorkOrderWriteSerializer

class WorkOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkOrder.objects.all()
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()] 
        return [IsAuthenticated(), IsAdminOrEngineer()]
    def get_serializer_class(self):
        return WorkOrderReadSerializer if self.request.method == 'GET' else WorkOrderWriteSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.assigned_to != request.user:
            raise PermissionDenied("Only the assigned engineer can update this work order.")

        if request.data.get('status') == 'closed' and not instance.completed_date:
            from django.utils import timezone
            instance.completed_date = timezone.now()

        return super().update(request, *args, **kwargs)

class SparePartRequestListCreateView(generics.ListCreateAPIView):
    queryset = SparePartRequest.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrEngineer]

    def get_serializer_class(self):
        return SparePartRequestReadSerializer if self.request.method == 'GET' else SparePartRequestWriteSerializer

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

class SparePartRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SparePartRequest.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrEngineer]

    def get_serializer_class(self):
        return SparePartRequestReadSerializer if self.request.method == 'GET' else SparePartRequestWriteSerializer

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request):
        activity = []

        for wo in WorkOrder.objects.order_by('-reported_date')[:2]:
            activity.append({
                "message": f"Work Order {wo.work_number} status: {wo.get_status_display()}",
                "timestamp": timesince(wo.reported_date, now()) + " ago"
            })

        for sp in SparePartRequest.objects.order_by('-request_date')[:2]:
            activity.append({
                "message": f"Spare Part Request {sp.request_number} ({sp.get_status_display()})",
                "timestamp": timesince(sp.request_date, now()) + " ago"
            })

        recent_activity = sorted(activity, key=lambda x: x['timestamp'])[:4]

        return Response({
            "total_hospitals": Hospital.objects.count(),
            "total_devices": Device.objects.count(),
            "total_work_orders": WorkOrder.objects.count(),
            "pending_spare_requests": SparePartRequest.objects.filter(status="pending").count(),
            "recent_activity": recent_activity
        })


class EngineerDashboardView(APIView):
    permission_classes = [IsAuthenticated & IsEngineerUser]

    def get(self, request):
        user = request.user

        total_assigned_devices = Device.objects.filter(assigned_engineer=user).count()
        my_work_orders = WorkOrder.objects.filter(assigned_to=user)
        total_my_work_orders = my_work_orders.count()
        total_open_work_orders = my_work_orders.filter(status="open").count()

        # Recent Activity
        activity = []

        for wo in my_work_orders.order_by('-reported_date')[:2]:
            activity.append({
                "message": f"Work Order {wo.work_number} status: {wo.get_status_display()}",
                "timestamp": timesince(wo.reported_date, now()) + " ago"
            })

        for sp in SparePartRequest.objects.filter(requested_by=user).order_by('-request_date')[:2]:
            activity.append({
                "message": f"Spare Part Request {sp.request_number} ({sp.get_status_display()})",
                "timestamp": timesince(sp.request_date, now()) + " ago"
            })

        recent_activity = sorted(activity, key=lambda x: x["timestamp"])[:4]

        return Response({
            "total_assigned_devices": total_assigned_devices,
            "total_my_work_orders": total_my_work_orders,
            "total_open_work_orders": total_open_work_orders,
            "recent_activity": recent_activity
        })

class NurseDashboardView(APIView):
    permission_classes = [IsAuthenticated & IsNurseUser]

    def get(self, request):
        user = request.user
        created_work_orders = WorkOrder.objects.filter(created_by=user)
        open_work_orders = created_work_orders.filter(status="open").count()
        closed_work_orders_qs = created_work_orders.filter(status="closed")
        closed_work_orders = closed_work_orders_qs.count()

        activity = []

        for wo in created_work_orders.order_by('-reported_date'):
            activity.append({
                "message": f"Work Order {wo.work_number} has been created",
                "timestamp": timesince(wo.reported_date, now()) + " ago"
            })

        for wo in closed_work_orders_qs.order_by('-completed_date'):
            activity.append({
                "message": f"Work Order {wo.work_number} has been closed",
                "timestamp": timesince(wo.completed_date or wo.reported_date, now()) + " ago"
            })

        recent_activity = sorted(activity, key=lambda x: x["timestamp"])[:4]

        return Response({
            "reported_work_orders": created_work_orders.count(),
            "open_work_orders": open_work_orders,
            "closed_work_orders": closed_work_orders,
            "recent_activity": recent_activity
        })

class UserListByTypeView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request):
        user_type = request.query_params.get('type')

        if user_type == 'engineer':
            engineers = Engineer.objects.select_related('user').all()
            users = [e.user for e in engineers]
        elif user_type == 'nurse':
            nurses = Nurse.objects.select_related('user').all()
            users = [n.user for n in nurses]
        elif user_type == 'admin':
            admins = Admin.objects.select_related('user').all()
            users = [a.user for a in admins]
        else:
            return Response({'error': 'Invalid user type.'}, status=400)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class AssignedDeviceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Only engineers are allowed to use this endpoint
        if not hasattr(user, 'engineer'):
            return Response(
                {'detail': 'Forbidden: Only engineers can access assigned devices.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get devices assigned to this engineer
        devices = Device.objects.filter(assigned_engineer=user)
        serializer = DeviceReadSerializer(devices, many=True)
        return Response(serializer.data)


class EngineerAssignedWorkOrders(APIView):
    permission_classes = [IsAuthenticated & IsEngineerUser]

    def get(self, request):
        work_orders = WorkOrder.objects.filter(assigned_to=request.user)
        serializer = WorkOrderReadSerializer(work_orders, many=True)
        return Response(serializer.data)

class EngineerOpenWorkOrdersView(generics.ListAPIView):
    serializer_class = WorkOrderReadSerializer
    permission_classes = [IsAuthenticated & IsEngineerUser]

    def get_queryset(self):
        return WorkOrder.objects.filter(
            assigned_to=self.request.user,
            status='open'
        )

class NurseWorkOrdersView(APIView):
    permission_classes = [IsAuthenticated & IsNurseUser]

    def get(self, request):
        user = request.user
        open_orders = WorkOrder.objects.filter(created_by=user, status='open')
        closed_orders = WorkOrder.objects.filter(created_by=user, status='closed')

        return Response({
            "open": WorkOrderReadSerializer(open_orders, many=True).data,
            "closed": WorkOrderReadSerializer(closed_orders, many=True).data
        })

