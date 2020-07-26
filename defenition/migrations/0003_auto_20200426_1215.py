# Generated by Django 2.2.6 on 2020-04-26 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('defenition', '0002_auto_20200409_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurancerule',
            name='global_flag',
        ),
        migrations.AlterField(
            model_name='insurancerule',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='InsuranceRule_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
