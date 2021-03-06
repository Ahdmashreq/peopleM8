# Generated by Django 2.2.6 on 2021-03-08 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0015_auto_20210301_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_Depandance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('relation', models.CharField(max_length=60, verbose_name='relationship')),
                ('mobile', models.CharField(blank=True, max_length=255, null=True, verbose_name='depandance mobile')),
                ('id_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Depandance ID')),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='depandance_created_by', to=settings.AUTH_USER_MODEL)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.Employee')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
