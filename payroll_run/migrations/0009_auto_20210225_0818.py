# Generated by Django 2.2.6 on 2021-02-25 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_run', '0008_auto_20210127_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary_elements',
            name='elements_type_to_run',
            field=models.CharField(blank=True, choices=[('appear', 'Payslip elements'), ('no_appear', 'Not payslip elements')], default='appear', max_length=50, null=True, verbose_name='Run on'),
        ),
    ]