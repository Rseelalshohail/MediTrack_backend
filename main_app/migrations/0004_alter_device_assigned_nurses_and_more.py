# Generated by Django 5.2 on 2025-05-06 09:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_device_assigned_nurses'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='assigned_nurses',
            field=models.ManyToManyField(blank=True, limit_choices_to={'user_type': 'nurse'}, related_name='devices_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='work_type',
            field=models.CharField(choices=[('CM', 'Corrective Maintenance (CM)'), ('PPM', 'Planned Preventive Maintenance (PPM)')], max_length=3),
        ),
    ]
