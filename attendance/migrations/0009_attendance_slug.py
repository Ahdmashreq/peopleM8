# Generated by Django 2.2.6 on 2020-07-29 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20200624_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
