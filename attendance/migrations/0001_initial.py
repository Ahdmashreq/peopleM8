# Generated by Django 2.2.6 on 2020-07-26 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('check_in', models.TimeField(blank=True, null=True)),
                ('check_out', models.TimeField(blank=True, null=True)),
                ('work_time', models.CharField(blank=True, max_length=100, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='attendance.Attendance')),
            ],
        ),
    ]
