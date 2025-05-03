from rest_framework import serializers
from .models import Admin, Engineer, Nurse, Hospital, Room, Device, WorkOrder, SparePartRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        Admin.objects.create(user=user)
        return user

class EngineerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        Engineer.objects.create(user=user)
        return user

class NurseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        Nurse.objects.create(user=user)
        return user

class DeviceReadSerializer(serializers.ModelSerializer):
    room_display = serializers.SerializerMethodField()
    assigned_engineer_display = serializers.SerializerMethodField()
    last_inventory_date = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Device
        fields = (
            'asset_number',
            'serial_number',
            'model',
            'manufacturer',
            'status',
            'room_display',
            'assigned_engineer_display',
            'last_inventory_date',
        )
        read_only_fields = ('id',)
    def get_room_display(self, obj):
        return str(obj.room) if obj.room else None
    def get_assigned_engineer_display(self, obj):
        return obj.assigned_engineer.username if obj.assigned_engineer else None
    
class DeviceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('id',)

class RoomSerializer(serializers.ModelSerializer):
    hospital = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('id',)

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
        read_only_fields = ('id',)

class WorkOrderReadSerializer(serializers.ModelSerializer):
    device_display = serializers.SerializerMethodField()
    created_by_display = serializers.SerializerMethodField()
    assigned_to_display = serializers.SerializerMethodField()
    reported_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    completed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        model = WorkOrder
        fields = (
            'id',
            'work_number',
            'description',
            'work_type',
            'status',
            'reported_date',
            'completed_date',
            'device_display',
            'created_by_display',
            'assigned_to_display',
        )
        read_only_fields = ('id', 'work_number',)
    def get_device_display(self, obj):
        return str(obj.device) if obj.device else None
    def get_created_by_display(self, obj):
        return obj.created_by.username if obj.created_by else None
    def get_assigned_to_display(self, obj):
        return obj.assigned_to.username if obj.assigned_to else None

class WorkOrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('id', 'work_number', 'reported_date', 'assigned_to', 'status', 'completed_date')
    def create(self, validated_data):
        validated_data['status'] = 'open'
        device = validated_data['device']
        if not device.assigned_engineer:
            raise serializers.ValidationError("This device has no assigned engineer.")
        validated_data['assigned_to'] = device.assigned_engineer
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)

class SparePartRequestReadSerializer(serializers.ModelSerializer):
    device_display = serializers.SerializerMethodField()
    requested_by_display = serializers.SerializerMethodField()
    requested_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = SparePartRequest
        fields = (
            'id',
            'request_number',
            'description',
            'quantity',
            'status',
            'requested_date',
            'device_display',
            'requested_by_display',
        )
    def get_device_display(self, obj):
        return str(obj.device) if obj.device else None
    def get_requested_by_display(self, obj):
        return obj.requested_by.username if obj.requested_by else None
        
class SparePartRequestWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePartRequest
        fields = '__all__'
        read_only_fields = ('id', 'request_number', 'requested_date')