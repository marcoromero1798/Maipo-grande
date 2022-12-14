# Generated by Django 3.2.6 on 2022-10-31 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_carro_compra_cc_nestado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='PC_NPRECIO',
        ),
        migrations.RemoveField(
            model_name='solicitud_compra',
            name='SCD_NMONTO_TOTAL',
        ),
        migrations.AddField(
            model_name='orden_venta',
            name='OV_FFECHA_PROCESAMIENTO',
            field=models.DateTimeField(blank=True, null=True, verbose_name='FECHA PROCESAMIENTO'),
        ),
        migrations.AddField(
            model_name='orden_venta',
            name='OV_NDOCUMENTO_ORIGEN',
            field=models.IntegerField(default=1, verbose_name='Documento origen'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orden_venta_detalle',
            name='OV_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.orden_venta', verbose_name='ID SOLICITUD OVD'),
        ),
    ]
