from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Hospital, Room, Device, WorkOrder, SparePartRequest, Admin, Engineer, Nurse

class ModelTests(TestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_user(username='admin1', password='pass')
        self.engineer_user = User.objects.create_user(username='engineer1', password='pass')
        self.nurse_user = User.objects.create_user(username='nurse1', password='pass')

        # User Type Profiles
        self.admin = Admin.objects.create(user=self.admin_user)
        self.engineer = Engineer.objects.create(user=self.engineer_user)
        self.nurse = Nurse.objects.create(user=self.nurse_user)

        # Hospital + Room
        self.hospital = Hospital.objects.create(name='City Hospital')
        self.room = Room.objects.create(room_number='101', hospital=self.hospital)

        # Device
        self.device = Device.objects.create(
            asset_number='A123',
            serial_number='SN123',
            equipment_name='Infusion Pump',
            model='IP-200',
            manufacturer='MedTech',
            room=self.room,
            status='active',
            assigned_engineer=self.engineer_user
        )
        self.device.assigned_nurses.set([self.nurse_user])

        # Work Order
        self.work_order = WorkOrder.objects.create(
            description='Pump not working',
            work_type='CM',
            device=self.device,
            created_by=self.nurse_user,
            assigned_to=self.engineer_user
        )

        # Spare Part Request
        self.spr = SparePartRequest.objects.create(
            part_name='Tube',
            description='Replacement tube needed',
            quantity=1,
            device=self.device,
            requested_by=self.nurse_user
        )

    def test_user_profiles_created(self):
        self.assertEqual(str(self.admin), 'Admin: admin1')
        self.assertEqual(str(self.engineer), 'Engineer: engineer1')
        self.assertEqual(str(self.nurse), 'Nurse: nurse1')

    def test_hospital_and_room(self):
        self.assertEqual(str(self.hospital), 'City Hospital')
        self.assertEqual(str(self.room), '101 - City Hospital')

    def test_device_creation(self):
        self.assertEqual(str(self.device), 'A123 - IP-200')

    def test_work_order_creation(self):
        self.assertTrue(self.work_order.work_number.startswith('WO-'))
        self.assertEqual(self.work_order.device, self.device)

    def test_spare_part_request_creation(self):
        self.assertTrue(self.spr.request_number.startswith('SPR-'))
        self.assertEqual(self.spr.device.asset_number, 'A123')
    def test_room_device_relationship(self):
        self.assertEqual(self.room.devices.count(), 1)

    def test_device_engineer_relationship(self):
        self.assertEqual(self.device.assigned_engineer.username, 'engineer1')

    def test_device_nurse_relationship(self):
        self.assertIn(self.nurse_user, self.device.assigned_nurses.all())

    def test_device_work_orders(self):
        self.assertEqual(self.device.work_orders.count(), 1)
    def test_delete_hospital_cascades_rooms(self):
        self.hospital.delete()
        self.assertEqual(Room.objects.count(), 0)

    def test_delete_device_cascades_work_orders(self):
        self.device.delete()
        self.assertEqual(WorkOrder.objects.count(), 0)

    def test_delete_user_cascades_profiles(self):
        self.nurse_user.delete()
        self.assertEqual(Nurse.objects.count(), 0)
