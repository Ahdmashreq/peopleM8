# Generated by Django 2.2.6 on 2020-09-03 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('check_in', models.TimeField(blank=True, null=True)),
                ('check_out', models.TimeField(blank=True, null=True)),
                ('work_hours', models.CharField(blank=True, max_length=100, null=True)),
                ('normal_hrs', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True)),
                ('normal_overtime_hours', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True)),
                ('exceptional_hrs', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True)),
                ('exceptional_overtime', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True)),
                ('delay_hrs', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=4, null=True)),
                ('absence_days', models.IntegerField(blank=True, default=0, null=True)),
                ('day_of_week', models.CharField(max_length=12)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance_Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('check_in', models.TimeField(blank=True, null=True)),
                ('check_out', models.TimeField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
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
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='attendance.Attendance')),
            ],
        ),
    ]
