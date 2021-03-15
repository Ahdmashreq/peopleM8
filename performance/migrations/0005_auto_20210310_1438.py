# Generated by Django 2.2.6 on 2021-03-10 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0004_auto_20210304_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.Performance')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.PerformanceRating')),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.Segment'),
        ),
        migrations.DeleteModel(
            name='PerformanceTitle',
        ),
    ]