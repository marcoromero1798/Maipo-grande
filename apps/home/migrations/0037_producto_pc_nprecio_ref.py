# Generated by Django 3.2.6 on 2022-11-02 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_alter_solicitud_compra_detalle_pc_nid'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='PC_NPRECIO_REF',
            field=models.DecimalField(decimal_places=5, default=1, max_digits=18, verbose_name='PRECIO REFERENCIA'),
            preserve_default=False,
        ),
    ]
