# Generated by Django 2.2.13 on 2021-01-11 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('defenition', '0001_initial'),
        ('element_definition', '0002_auto_20210111_0859'),
        ('manage_payroll', '0001_initial'),
        ('company', '0002_auto_20210111_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='element_link',
            name='payroll_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_payroll.Payroll_Master', verbose_name='Payroll'),
        ),
        migrations.AddField(
            model_name='element_batch_master',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='element_batch_master',
            name='element_batch_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_batch_fk', related_query_name='elementBatch', to='element_definition.Element_Batch', verbose_name='Pay Batch'),
        ),
        migrations.AddField(
            model_name='element_batch_master',
            name='element_master_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_master_fk', related_query_name='elementMaster', to='element_definition.Element_Master', verbose_name='Pay'),
        ),
        migrations.AddField(
            model_name='element_batch_master',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='element_batch',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_batch_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='element_batch',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_batch_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='element_batch',
            name='payroll_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_payroll.Payroll_Master', verbose_name='Payroll'),
        ),
        migrations.AddField(
            model_name='element',
            name='based_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='element_definition.Element'),
        ),
        migrations.AddField(
            model_name='element',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_lookup_classification', to='defenition.LookupDet', verbose_name='classification'),
        ),
        migrations.AddField(
            model_name='element',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_is_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='element',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_salary_elements', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='element',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_is_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='custom_python_rule',
            name='element_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_python_rule', to='element_definition.Element_Master', verbose_name='Pay Master'),
        ),
        migrations.AlterUniqueTogether(
            name='element_link',
            unique_together={('element_master_fk', 'employee')},
        ),
    ]
