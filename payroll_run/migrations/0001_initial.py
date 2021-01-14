# Generated by Django 2.2.6 on 2020-11-01 11:43

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('element_definition', '0002_auto_20201101_1143'),
        ('manage_payroll', '0001_initial'),
        ('employee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary_elements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='Salary Month')),
                ('salary_year', models.IntegerField(verbose_name='Salary Year')),
                ('run_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Run Date')),
                ('num_days', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Number of Days')),
                ('incomes', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Income')),
                ('insurance_amount', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Insurance Amount')),
                ('tax_amount', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Tax Amount')),
                ('deductions', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Deduction')),
                ('gross_salary', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Gross Salary')),
                ('net_salary', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Net Salary')),
                ('is_final', models.BooleanField(blank=True, default=False, verbose_name='Salary is final')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('creation_date', models.DateField(auto_now=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
                ('assignment_batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_payroll.Assignment_Batch', verbose_name='Assignment Batch')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_created_by', to=settings.AUTH_USER_MODEL)),
                ('element_batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='element_definition.Element_Batch', verbose_name='Element Batch')),
                ('emp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', verbose_name='Employee')),
                ('last_update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_last_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('emp', 'salary_month', 'salary_year', 'is_final')},
            },
        ),
    ]
