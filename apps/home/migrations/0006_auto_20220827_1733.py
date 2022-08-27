# Generated by Django 3.2.6 on 2022-08-27 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20220827_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categariaproducto',
            name='CP_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='cliente_externo',
            name='CLE_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='cliente_interno',
            name='CLI_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='consultor',
            name='CON_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='CT_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='PC_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='productor',
            name='PR_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
        migrations.AlterField(
            model_name='transportista',
            name='TR_NHABILITADO',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
    ]
