# Generated by Django 2.2.6 on 2020-07-26 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0001_initial'),
        ('leave', '0001_initial'),
        ('employee', '0002_auto_20200726_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='message content')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='delivered', max_length=20)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('bussiness_travel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_bussiness_travel', to='service.Bussiness_Travel')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Notification_created_by', to=settings.AUTH_USER_MODEL)),
                ('from_emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to='employee.Employee', verbose_name='Employee')),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Notification_last_updated_by', to=settings.AUTH_USER_MODEL)),
                ('leave', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_leave', to='leave.Leave')),
                ('to_emp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_to', to='employee.Employee', verbose_name='Employee')),
            ],
        ),
    ]
