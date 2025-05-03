from django.urls import path
from .views import Home, AdminSignupView, EngineerSignupView, NurseSignupView, LoginView, HospitalListCreateView, HospitalDetailView, RoomListCreateView, RoomDetailView, DeviceListCreateView, DeviceDetailView, WorkOrderListCreateView, WorkOrderDetailView, SparePartRequestListCreateView, SparePartRequestDetailView

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
]