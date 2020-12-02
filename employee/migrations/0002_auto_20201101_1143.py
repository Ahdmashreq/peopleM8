# Generated by Django 2.2.6 on 2020-11-01 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_auto_20201101_1143'),
        ('defenition', '0001_initial'),
        ('employee', '0001_initial'),
        ('manage_payroll', '0001_initial'),
        ('element_definition', '0003_auto_20201101_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emp_payment_method', to='manage_payroll.Payment_Method', verbose_name='Payment Method'),
        ),
        migrations.AddField(
            model_name='medical',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medical',
            name='emp_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='medical',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='contract_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobroll_contract_type', to='defenition.LookupDet', verbose_name='Contract Type'),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobRoll_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='emp_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_roll_emp_id', to='employee.Employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobroll_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager_id', to='employee.Employee', verbose_name='Manager'),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='payroll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_payroll.Payroll_Master', verbose_name='Payroll'),
        ),
        migrations.AddField(
            model_name='jobroll',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Position', verbose_name='Position'),
        ),
        migrations.AddField(
            model_name='employee_element',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emp_element_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee_element',
            name='element_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='element_definition.Element_Master', verbose_name='Element'),
        ),
        migrations.AddField(
            model_name='employee_element',
            name='emp_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='employee_element',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_element_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emp_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_employee', to='company.Enterprise', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_user', to=settings.AUTH_USER_MODEL),
        ),
    ]