# Generated by Django 2.2.6 on 2021-03-15 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('element_definition', '0017_remove_elementformula_based_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementformula',
            name='based_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='element_based_on', to='element_definition.Element'),
        ),
    ]
