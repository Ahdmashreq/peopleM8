# Generated by Django 2.2.6 on 2021-03-04 11:03

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0002_auto_20210304_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performancerating',
            name='score_key',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='1', max_length=11),
        ),
    ]