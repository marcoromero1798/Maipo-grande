# Generated by Django 3.2.6 on 2022-11-03 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_auto_20221102_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='subasta',
            name='OV_NDOCUMENTO_ORIGEN',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.orden_venta', verbose_name='Documento origen'),
        ),
        migrations.AddField(
            model_name='subasta_detalle',
            name='SU_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.subasta', verbose_name='ID SUBASTA'),
        ),
        migrations.AlterField(
            model_name='categariaproducto',
            name='CP_FOTO',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='PC_FOTO',
            field=models.ImageField(upload_to='images'),
        ),
    ]
