# Generated by Django 3.2.6 on 2022-11-02 06:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_producto_pc_nprecio_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='PC_FFECHA_VENCIMIENTO',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha TERMINO'),
            preserve_default=False,
        ),
    ]
