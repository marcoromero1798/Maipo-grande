# Generated by Django 3.2.6 on 2022-10-31 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20221031_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden_venta',
            name='OV_CTIPO_PROCESO',
            field=models.CharField(default=1, max_length=50, verbose_name='Tipo Documento'),
            preserve_default=False,
        ),
    ]
