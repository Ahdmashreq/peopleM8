# Generated by Django 2.2.6 on 2020-04-01 16:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=150, verbose_name='Department')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start  Date')),
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
            ],
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('business_unit_name', models.CharField(max_length=150, verbose_name='Business Unit Name')),
                ('reg_tax_num', models.CharField(max_length=150, verbose_name='Reg Tax Num')),
                ('commercail_record', models.CharField(max_length=150, verbose_name='Commercail Record ')),
                ('address1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address1')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone')),
                ('mobile', models.CharField(blank=True, max_length=255, null=True, verbose_name='Mobile')),
                ('fax', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fax')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
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
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name', models.CharField(max_length=100, verbose_name='Grade Name')),
                ('grade_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Grade Description')),
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
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=100, verbose_name='Job Name')),
                ('job_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Job Description')),
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
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=100, verbose_name='Position Name')),
                ('position_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Position Description')),
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
            ],
        ),
    ]
