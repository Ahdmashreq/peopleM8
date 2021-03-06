# Generated by Django 2.2.13 on 2021-01-25 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task_management', '0009_auto_20210117_1530'),
        ('employee', '0011_merge_20210113_1550'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0005_merge_20210113_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('check_in', models.TimeField(blank=True, null=True)),
                ('check_out', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('work_hours', models.CharField(blank=True, max_length=100, null=True)),
                ('normal_hrs', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True)),
                ('normal_overtime_hours', models.DurationField(blank=True, null=True)),
                ('exceptional_hrs', models.TimeField(blank=True, null=True)),
                ('exceptional_overtime', models.TimeField(blank=True, null=True)),
                ('delay_hrs', models.DurationField(blank=True, null=True)),
                ('absence_days', models.IntegerField(blank=True, default=0, null=True)),
                ('day_of_week', models.CharField(blank=True, max_length=12, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_created_by', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_attendance', to='employee.Employee')),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='attendance.Attendance')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_last_updated_by', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to='task_management.Project_Task')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee_Attendance_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.PositiveIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('year', models.PositiveIntegerField()),
                ('attendance_days', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('leave_days', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('absence_days', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_attendance_history_created_by', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_attendance_history_employee', to='employee.Employee')),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_attendance_history_last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance_Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=250)),
                ('user_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField()),
                ('punch', models.CharField(max_length=3)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Enterprise')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_interface_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_interface_last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
