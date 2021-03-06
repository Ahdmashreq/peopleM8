# Generated by Django 2.2.13 on 2021-02-07 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('balanc_definition', '0002_auto_20210207_1023'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_auto_20210207_1023'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost_center_link',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', verbose_name='Employee Name'),
        ),
        migrations.AddField(
            model_name='cost_center_link',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Grade', verbose_name='Grade'),
        ),
        migrations.AddField(
            model_name='cost_center_link',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Job', verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='cost_center_link',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_center_link_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
