from django.urls import path
from .views import Home, AdminSignupView, EngineerSignupView, NurseSignupView, LoginView, HospitalListCreateView, HospitalDetailView, RoomListCreateView, RoomDetailView, DeviceListCreateView, DeviceDetailView, WorkOrderListCreateView, WorkOrderDetailView, SparePartRequestListCreateView, SparePartRequestDetailView, AdminDashboardView, EngineerDashboardView, NurseDashboardView, UserListByTypeView, AssignedDeviceListView, EngineerAssignedWorkOrders, EngineerOpenWorkOrdersView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup/admin/', AdminSignupView.as_view(), name='signup-admin'),
    path('signup/engineer/', EngineerSignupView.as_view(), name='signup-engineer'),
    path('signup/nurse/', NurseSignupView.as_view(), name='signup-nurse'),
    path('token/', LoginView.as_view(), name='token'),
    path('hospitals/', HospitalListCreateView.as_view(), name='hospital-list-create'),
    path('hospitals/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('workorders/', WorkOrderListCreateView.as_view(), name='workorder-list-create'),
    path('workorders/<int:pk>/', WorkOrderDetailView.as_view(), name='workorder-detail'),
    path('spareparts/', SparePartRequestListCreateView.as_view(), name='sparepart-list-create'),
    path('spareparts/<int:pk>/', SparePartRequestDetailView.as_view(), name='sparepart-detail'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='dashboard-admin'),
    path('dashboard/engineer/', EngineerDashboardView.as_view(), name='dashboard-engineer'),
    path('dashboard/nurse/', NurseDashboardView.as_view(), name='dashboard-nurse'),
    path('users/', UserListByTypeView.as_view(), name='user-list-by-type'),
    path('devices/assigned/', AssignedDeviceListView.as_view(), name='assigned-devices'),
    path('workorders/assigned/', EngineerAssignedWorkOrders.as_view(), name='engineer-workorders'),
    path('workorders/open/', EngineerOpenWorkOrdersView.as_view(), name='open-workorders'),
]