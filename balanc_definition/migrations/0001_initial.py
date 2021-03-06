# Generated by Django 2.2.13 on 2021-01-11 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cost_Center',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_center', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Cost Center')),
                ('account_number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Account Number')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cost_Center_Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cost_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_account', models.CharField(blank=True, max_length=50, null=True, verbose_name='Debit Account')),
                ('credit_account', models.CharField(blank=True, max_length=50, null=True, verbose_name='Credit Account')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cost_Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(choices=[('D', 'Department'), ('J', 'Jobs'), ('G', 'Grade'), ('P', 'Position')], max_length=50, verbose_name='Level Name')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
