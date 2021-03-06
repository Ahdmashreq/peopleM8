# Generated by Django 2.2.6 on 2020-12-08 11:29

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20201101_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Department', verbose_name='Reporting Department'),
        ),
    ]
