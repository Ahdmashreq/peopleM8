# Generated by Django 2.2.6 on 2020-09-03 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20200903_1244'),
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to='company.Enterprise', verbose_name='Name'),
        ),
    ]
