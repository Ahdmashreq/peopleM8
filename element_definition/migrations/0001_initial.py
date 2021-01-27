# Generated by Django 2.2.6 on 2020-11-01 11:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_auto_20201101_1143'),
        ('defenition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_Python_Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('help_text', models.TextField(default='\n    You can define a custom deduction/addition rule here using python code.\n    You have the following variables available to use:\n    * basic: this is the basic salary of the employee.\n    * variable: this is the variable salary of the employee.\n    * d_days: these are the number of days the employee should be deducted this month\n    because of his/her absence or any other Attendance rules that implies deduction days.\n    * grs:(without `o`) gross salary equals to basic salary + variable salary + any other added allowances/bonus/incentive etc..\n    After calculating your equation, you have to store the required amount to be added/deducted in a variable named amount.\n    If the value of the amount variable is positive, the amount will be added to the net salary of the employee.\n    And if it is negative, it will be deducted.\n    Example:\n    if basic <= 5000:\n    ____extra_deduction = -250\n    else:\n    ____extra_deduction = -500\n    amount = extra_deduction\n    Make Sure that your code is properly indented using 4 spaces\n    ', verbose_name='Help Text')),
                ('rule_definition', models.TextField(verbose_name='Rule Definition')),
                ('taxable', models.BooleanField(default=False, verbose_name='Taxable')),
            ],
        ),
        migrations.CreateModel(
            name='Element_Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.CharField(max_length=255, verbose_name='Batch Name')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Element_Batch_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Element_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_parameter_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Parameter Name')),
                ('user_enterable', models.BooleanField(verbose_name='User Enterable')),
                ('required', models.BooleanField(verbose_name='Required')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Element_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_name', models.CharField(max_length=100, verbose_name='Name')),
                ('db_name', models.CharField(blank=True, max_length=4, null=True, verbose_name='db Name')),
                ('effective_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Effective Date')),
                ('retro_flag', models.BooleanField(verbose_name='Retro Flag')),
                ('tax_flag', models.BooleanField(verbose_name='Tax Flag')),
                ('fixed_amount', models.IntegerField(default=0, verbose_name='Fixed Amount')),
                ('element_formula', models.TextField(blank=True, max_length=255, null=True, verbose_name='Formula')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
                ('classification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lookup_classification', to='defenition.LookupDet', verbose_name='classification')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_master_created_by', to=settings.AUTH_USER_MODEL)),
                ('element_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lookup_element', to='defenition.LookupDet', verbose_name='Element Type')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_element_master', to='company.Enterprise', verbose_name='Enterprise Name')),
                ('last_update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_master_last_update_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Element_Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_flag', models.BooleanField(blank=True, default=False, verbose_name='Standard Flag')),
                ('link_to_all_payroll_flag', models.BooleanField(blank=True, default=False, verbose_name='Link All')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='element_definition.Element_Batch', verbose_name='Batch Name')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_link_created_by', to=settings.AUTH_USER_MODEL)),
                ('element_dept_id_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Department', verbose_name='Department')),
                ('element_grade_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Grade', verbose_name='Grade')),
                ('element_job_id_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Job', verbose_name='Job')),
                ('element_master_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_link_to_master', to='element_definition.Element_Master', verbose_name='Element Name')),
                ('element_position_id_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Position', verbose_name='Position')),
            ],
        ),
    ]
