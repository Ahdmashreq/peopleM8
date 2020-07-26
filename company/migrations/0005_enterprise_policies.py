# Generated by Django 2.2.6 on 2020-06-15 13:08

import company.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0004_remove_enterprise_business_unit_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise_Policies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Policy Description')),
                ('attachment', models.ImageField(blank=True, null=True, upload_to=company.models.path_and_rename, verbose_name='Attachment')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
                ('attribute1', models.CharField(max_length=255)),
                ('attribute2', models.CharField(max_length=255)),
                ('attribute3', models.CharField(max_length=255)),
                ('attribute4', models.CharField(max_length=255)),
                ('attribute5', models.CharField(max_length=255)),
                ('attribute6', models.CharField(max_length=255)),
                ('attribute7', models.CharField(max_length=255)),
                ('attribute8', models.CharField(max_length=255)),
                ('attribute9', models.CharField(max_length=255)),
                ('attribute10', models.CharField(max_length=255)),
                ('attribute11', models.CharField(max_length=255)),
                ('attribute12', models.CharField(max_length=255)),
                ('attribute13', models.CharField(max_length=255)),
                ('attribute14', models.CharField(max_length=255)),
                ('attribute15', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policy_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policy_last_update_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
