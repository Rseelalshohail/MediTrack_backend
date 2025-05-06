from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Admin (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__ (self):
        return f"Admin: {self.user.username}"
    
class Engineer (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__ (self):
        return f"Engineer: {self.user.username}"
    
class Nurse (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__ (self):
        return f"Nurse: {self.user.username}"
#-------------------------------------------
class Hospital (models.Model):
    name = models.CharField(max_length=150)
    
    def __str__ (self):
        return self.name
    
class Room (models.Model):
    room_number = models.CharField(max_length=20)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='rooms')
    
    class Meta:
        unique_together = ('room_number', 'hospital')
        
    def __str__ (self):
        return f"{self.room_number} - {self.hospital.name}"
#-------------------------------------------
class Device (models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ]
    asset_number = models.CharField(max_length=50, unique=True)
    serial_number = models.CharField(max_length=50)
    equipment_name = models.CharField(max_length=200)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    assigned_engineer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_devices'
    )
    assigned_nurses = models.ManyToManyField(User, blank=True, related_name="devices_assigned", limit_choices_to={"user_type": "nurse"})
    last_inventory_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.asset_number} - {self.model}"
#-------------------------------------------
class WorkOrder(models.Model):
    TYPE_CHOICES = [
        ("CM", "Corrective Maintenance (CM)"),
        ("PPM", "Planned Preventive Maintenance (PPM)"),
    ]
    
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]
    
    work_number = models.CharField(max_length=50, unique=True, editable=False)
    description = models.TextField()
    work_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="open")
    reported_date = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="work_orders")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_work_orders")
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_work_orders"
        )
    
    def save (self, *args, **kwargs):
        if not self.work_number:
            year = timezone.now().year
            month = timezone.now().month
            prefix = f"WO-{year}{month:02d}"
            
            last_order = WorkOrder.objects.filter(work_number__startswith=prefix).order_by("work_number").last()
            last_number = int(last_order.work_number.split("-")[-1]) if last_order else 0
            self.work_number = f"{prefix}-{last_number + 1:04d}"
            
        if self.status == "closed" and not self.completed_date:
            self.completed_date = timezone.now()
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.work_number} - {self.get_work_type_display()} - {self.device.asset_number}"
    #-------------------------------------------
class SparePartRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    request_number = models.CharField(max_length=20, unique=True, editable=False)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    request_date = models.DateTimeField(default=timezone.now)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="spare_part_requests")
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="spare_part_requests")
    
    def save (self, *args, **kwargs):
        if not self.request_number:
            year = timezone.now().year
            month = timezone.now().month
            prefix = f"SPR-{year}{month:02d}"
            
            last_request = SparePartRequest.objects.filter(request_number__startswith=prefix).order_by("request_number").last()
            last_number = int(last_request.request_number.split("-")[-1]) if last_request else 0
            self.request_number = f"{prefix}-{last_number + 1:04d}"
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.request_number} - {self.description[:30]}"