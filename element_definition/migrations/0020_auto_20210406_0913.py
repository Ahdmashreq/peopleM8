# Generated by Django 2.2.13 on 2021-04-06 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('element_definition', '0019_merge_20210330_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementformula',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=200, null=True),
        ),
    ]
