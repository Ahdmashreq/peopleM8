# Generated by Django 2.2.6 on 2021-03-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0003_auto_20210304_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performancerating',
            name='score_key',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='1', max_length=25),
        ),
    ]
