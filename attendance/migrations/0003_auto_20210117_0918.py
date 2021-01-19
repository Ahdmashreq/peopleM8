# Generated by Django 2.2.13 on 2021-01-17 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
        ('attendance', '0002_auto_20210117_0918'),
        ('company', '0002_auto_20210117_0918'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_attendance_history',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_attendance_history_employee', to='employee.Employee'),
        ),
        migrations.AddField(
            model_name='employee_attendance_history',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_attendance_history_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance_interface',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Enterprise'),
        ),
        migrations.AddField(
            model_name='attendance_interface',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_interface_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance_interface',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_interface_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_attendance', to='employee.Employee'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]