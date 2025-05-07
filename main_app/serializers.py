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
    assigned_nurses_display = serializers.SerializerMethodField()
    assigned_nurses = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    last_inventory_date = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Device
        fields = (
            'id',
            'asset_number',
            'serial_number',
            'equipment_name',
            'model',
            'manufacturer',
            'status',
            'room_display',
            'assigned_engineer_display',
            'assigned_nurses_display',
            'assigned_nurses',
            'last_inventory_date',
        )
        read_only_fields = ('id',)
    def get_room_display(self, obj):
        return str(obj.room) if obj.room else None
    def get_assigned_engineer_display(self, obj):
        return obj.assigned_engineer.username if obj.assigned_engineer else None
    def get_assigned_nurses_display(self, obj):
        return [nurse.username for nurse in obj.assigned_nurses.all()]


    
class DeviceWriteSerializer(serializers.ModelSerializer):
    assigned_nurses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(nurse__isnull=False)  # Filter only nurses
    )

    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        assigned_nurses = validated_data.pop('assigned_nurses', [])
        device = super().create(validated_data)
        device.assigned_nurses.set(assigned_nurses)
        return device

    def update(self, instance, validated_data):
        assigned_nurses = validated_data.pop('assigned_nurses', None)
        device = super().update(instance, validated_data)
        if assigned_nurses is not None:
            device.assigned_nurses.set(assigned_nurses)
        return device


class RoomSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)  
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'hospital', 'hospital_name'] 
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
    assigned_to_id = serializers.IntegerField(source='assigned_to.id', read_only=True)
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    reported_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    completed_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)
    technical_action = serializers.CharField(read_only=True)
    photo = serializers.ImageField(read_only=True)

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
            'assigned_to_id',    
            'created_by_id', 
            'technical_action', 
            'photo', 
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
        read_only_fields = ('id', 'work_number', 'reported_date', 'assigned_to')
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
    request_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = SparePartRequest
        fields = (
            'id',
            'request_number',
            'part_name',
            'description',
            'quantity',
            'status',
            'request_date',
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
        read_only_fields = ('id', 'request_number', 'request_date')