# Generated by Django 5.2 on 2025-05-07 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_workorder_technical_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='work_order_photos/'),
        ),
    ]
