# Generated by Django 2.2.6 on 2020-07-26 14:24

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Employee Number')),
                ('emp_name', models.CharField(max_length=60, verbose_name='Employee Name')),
                ('address1', models.CharField(blank=True, max_length=255, null=True, verbose_name='address1')),
                ('address2', models.CharField(blank=True, max_length=255, null=True, verbose_name='address2')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='phone')),
                ('mobile', models.CharField(blank=True, max_length=255, null=True, verbose_name='mobile')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Birthdate')),
                ('hiredate', models.DateField(default=datetime.date.today, verbose_name='Hire Date')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='picture')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Is Active')),
                ('identification_type', models.CharField(blank=True, choices=[('N', 'National Id'), ('P', 'Passport')], max_length=5, null=True, verbose_name='ID Type')),
                ('id_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='ID Number')),
                ('place_of_birth', models.CharField(blank=True, max_length=100, null=True, verbose_name='Place of Birth')),
                ('nationality', models.CharField(blank=True, max_length=20, null=True, verbose_name='Nationality')),
                ('field_of_study', models.CharField(blank=True, max_length=30, null=True, verbose_name='Field of Study')),
                ('education_degree', models.CharField(blank=True, max_length=30, null=True, verbose_name='Eductaion Degree')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=5, null=True, verbose_name='Gender')),
                ('social_status', models.CharField(blank=True, choices=[('M', 'Married'), ('S', 'Single')], max_length=5, null=True, verbose_name='Social Status')),
                ('military_status', models.CharField(blank=True, choices=[('E', 'Exemption'), ('C', 'Complete the service'), ('P', 'Postponed')], max_length=5, null=True, verbose_name='Milatery Status')),
                ('religion', models.CharField(blank=True, choices=[('M', 'Muslim'), ('C', 'Chrestin')], max_length=5, null=True, verbose_name='Religion')),
                ('insured', models.BooleanField(verbose_name='Insured')),
                ('insurance_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Insurance Number')),
                ('insurance_date', models.DateField(blank=True, null=True, verbose_name='Insurance Date')),
                ('has_medical', models.BooleanField(verbose_name='Has Medical')),
                ('medical_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Medical Number')),
                ('medical_date', models.DateField(blank=True, null=True, verbose_name='Medical Date')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee_Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_value', models.FloatField(blank=True, null=True, verbose_name='Element Value')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobRoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_code', models.CharField(max_length=20, verbose_name='Medical Code')),
                ('medical_name', models.CharField(max_length=20, verbose_name='Medical Name')),
                ('medical_company', models.CharField(max_length=20, verbose_name='Medical Company')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Account Number')),
                ('percentage', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Percentage')),
                ('bank_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Bank Name')),
                ('swift_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Swift Code')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_created_by', to=settings.AUTH_USER_MODEL)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', verbose_name='Employee')),
                ('last_update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
