# Generated by Django 2.2 on 2021-03-11 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0017_merge_20210311_1358'),
        ('service', '0007_merge_20210311_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bussiness_travel',
            name='manager',
        ),
        migrations.AddField(
            model_name='bussiness_travel',
            name='approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_user', to='employee.Employee'),
        ),
        migrations.AddField(
            model_name='purchase_request',
            name='approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_emp', to='employee.Employee'),
        ),
        migrations.AddField(
            model_name='purchase_request',
            name='emp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp', to='employee.Employee', verbose_name='Employee Name'),
        ),
        migrations.AlterField(
            model_name='purchase_item',
            name='item_description',
            field=models.CharField(default='handel error', max_length=250),
        ),
        migrations.AlterField(
            model_name='purchase_item',
            name='qnt',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='purchase_item',
            name='unit_price',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='purchase_item',
            name='vendor_name',
            field=models.CharField(default='handel error', max_length=250),
        ),
    ]
