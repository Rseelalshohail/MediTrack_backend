from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser, IsEngineerUser, IsNurseUser, IsAdminOrEngineer, IsAdminOrNurse
from .models import Hospital, Room, Device, WorkOrder, SparePartRequest
from .serializers import (
    HospitalSerializer, RoomSerializer, DeviceReadSerializer, DeviceWriteSerializer,
    WorkOrderReadSerializer, WorkOrderWriteSerializer, SparePartRequestReadSerializer,
    SparePartRequestWriteSerializer, AdminSerializer, EngineerSerializer, NurseSerializer
)
# Define the home view
class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Admin created successfully", 
                            "username": user.username,
                            "id": user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EngineerSignupView(APIView):
    def post(self, request):
        serializer = EngineerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Engineer created successfully", 
                            "username": user.username,
                            "id": user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NurseSignupView(APIView):
    def post(self, request):
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Nurse created successfully", 
                            "username": user.username,
                            "id": user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        user_type = None
        if hasattr(user, 'admin'):
            user_type = 'admin'
        elif hasattr(user, 'engineer'):
            user_type = 'engineer'
        elif hasattr(user, 'nurse'):
            user_type = 'nurse'

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "username": user.username,
            "user_type": user_type,
        })

class Home(APIView):
    def get(self, request):
        content = {
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
            "login": "/api/token/"
},
            "version": "v1.0",
            "status": "API is running ✅"
        }
        return Response(content)
    
class HospitalListCreateView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

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
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceReadSerializer
        return DeviceWriteSerializer

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceReadSerializer
        return DeviceWriteSerializer
class WorkOrderListCreateView(generics.ListCreateAPIView):
    queryset = WorkOrder.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrNurse]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkOrderReadSerializer
        return WorkOrderWriteSerializer
    
class WorkOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkOrder.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrEngineer]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkOrderReadSerializer
        return WorkOrderWriteSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.assigned_to != request.user:
            raise PermissionDenied("Only the assigned engineer can update this work order.")

        data = request.data.copy()
        if data.get('status') == 'closed' and not instance.completed_date:
            from django.utils import timezone
            instance.completed_date = timezone.now()

        return super().update(request, *args, **kwargs)

class SparePartRequestListCreateView(generics.ListCreateAPIView):
    queryset = SparePartRequest.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrEngineer]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SparePartRequestReadSerializer
        return SparePartRequestWriteSerializer
    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

class SparePartRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SparePartRequest.objects.all()
    permission_classes = [IsAuthenticated & IsAdminOrEngineer]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SparePartRequestReadSerializer
        return SparePartRequestWriteSerializer