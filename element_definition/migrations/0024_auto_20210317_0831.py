# Generated by Django 2.2.6 on 2021-03-17 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('element_definition', '0023_merge_20210317_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementformula',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=200, null=True),
        ),
    ]