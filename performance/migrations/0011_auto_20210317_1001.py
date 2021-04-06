# Generated by Django 2.2.6 on 2021-03-17 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0010_auto_20210317_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('text', 'text'), ('slider', 'slider')], max_length=25),
        ),
        migrations.AlterField(
            model_name='segment',
            name='performance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Segments', to='performance.Performance'),
        ),
    ]