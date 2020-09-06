# Generated by Django 2.2.6 on 2020-09-03 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import leave.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Leave Type Name')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LeaveMaster_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LeaveMaster_last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(null=True, verbose_name='Start Date')),
                ('enddate', models.DateField(null=True, verbose_name='End Date')),
                ('resume_date', models.DateField(null=True, verbose_name='Resume Date')),
                ('leavetype', models.CharField(choices=[('A', 'Annual Leave'), ('S', 'Sick Leave'), ('C', 'Casual Leave'), ('U', 'Unpaid Leave'), ('M', 'Maternity/Paternity'), ('O', 'Other')], max_length=3, verbose_name='Leave Type Name')),
                ('reason', models.CharField(blank=True, help_text='add additional information for leave', max_length=255, null=True, verbose_name='Reason for Leave')),
                ('attachment', models.ImageField(blank=True, null=True, upload_to=leave.models.path_and_rename, verbose_name='Attachment')),
                ('status', models.CharField(default='pending', max_length=20)),
                ('is_approved', models.BooleanField(default=False)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Leave_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Leave_last_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
