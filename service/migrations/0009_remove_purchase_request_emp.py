# Generated by Django 2.2 on 2021-03-11 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20210311_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase_request',
            name='emp',
        ),
    ]
