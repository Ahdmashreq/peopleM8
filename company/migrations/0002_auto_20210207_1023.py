# Generated by Django 2.2.13 on 2021-02-07 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0008_city_timezone'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='yearlyholiday',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holiday_policy_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='yearlyholiday',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_yearly_holidays', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='yearlyholiday',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holiday_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='yearlyholiday',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Year', verbose_name='Year'),
        ),
        migrations.AddField(
            model_name='year',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='year_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='year',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_year', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='year',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='year_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='working_hours_deductions_policy',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_hr_deductions_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='working_hours_deductions_policy',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='working_hr_deductions_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='working_hours_deductions_policy',
            name='working_days_policy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Working_Days_Policy'),
        ),
        migrations.AddField(
            model_name='working_days_policy',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_hr_policy_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='working_days_policy',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_working_hrs_policy', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='working_days_policy',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='working_hr_policy_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='position',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='position',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_dept_fk', to='company.Department', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='position',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_grade_fk', to='company.Grade', verbose_name='Grade'),
        ),
        migrations.AddField(
            model_name='position',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_job_fk', to='company.Job', verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='position',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='job',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='job',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_enterprise', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='job',
            name='job_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='job',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grade',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grade',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_enterprise', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='grade',
            name='grade_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grade',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterprise_policies',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policy_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterprise_policies',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policy_enterprise', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='enterprise_policies',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policy_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='enterprise_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='department_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_enterprise', to='company.Enterprise', verbose_name='Enterprise Name'),
        ),
        migrations.AddField(
            model_name='department',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Department', verbose_name='Reporting Department'),
        ),
        migrations.AlterUniqueTogether(
            name='working_hours_deductions_policy',
            unique_together={('working_days_policy', 'day_number')},
        ),
        migrations.AlterUniqueTogether(
            name='working_days_policy',
            unique_together={('enterprise', 'week_end_days')},
        ),
    ]
