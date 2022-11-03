# Generated by Django 3.2.6 on 2022-11-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_auto_20221101_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud_compra_detalle',
            name='SCD_NMONTO',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='MONTO TOTAL'),
        ),
        migrations.AlterField(
            model_name='solicitud_compra_detalle',
            name='SCD_NPRECIO',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='PRECIO'),
        ),
    ]
