# Generated by Django 4.0.1 on 2022-02-26 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_control', '0001_initial'),
        ('equipment_control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='customer_control.address'),
        ),
        migrations.AddField(
            model_name='report',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='customer_control.contact'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='customer_control.customer'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='marca',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='report',
            name='parts',
            field=models.JSONField(default=list),
        ),
    ]
