# Generated by Django 3.2.6 on 2022-08-27 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20220827_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='PC_CUNIDAD_PESO',
            field=models.CharField(default=1, max_length=128, verbose_name='UNIDAD PESO'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='PC_NPESO',
            field=models.DecimalField(decimal_places=5, default=1, max_digits=18, verbose_name='Cantidad unidad de venta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='PC_NHABILITADO',
            field=models.BooleanField(default=True, verbose_name='Habilitado'),
        ),
        migrations.CreateModel(
            name='PARAMETRO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PM_CGRUPO', models.CharField(max_length=128, verbose_name='Grupo Parametro')),
                ('PM_CCODIGO', models.CharField(max_length=128, verbose_name='Codigo Parametro')),
                ('PM_CDESCRIPCION', models.CharField(max_length=1024, verbose_name='Descripcion')),
                ('PM_CVALOR1', models.CharField(max_length=1024, verbose_name='Valor Texto 1')),
                ('PM_CVALOR2', models.CharField(max_length=1024, verbose_name='Valor Texto 2')),
                ('PM_CVALOR3', models.CharField(max_length=1024, verbose_name='Valor Texto 3')),
                ('PM_NVALOR1', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Valor Numerico 1')),
                ('PM_NVALOR2', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Valor Numerico 2')),
                ('PM_NVALOR3', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Valor Numerico 3')),
            ],
            options={
                'db_table': 'PARAMETRO',
                'unique_together': {('PM_CGRUPO', 'PM_CCODIGO')},
            },
        ),
    ]
