# Generated by Django 2.2.13 on 2021-04-04 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0012_merge_20210404_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeabsence',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeeabsence',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]