# Generated by Django 3.2.6 on 2022-11-04 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0053_subasta_su_ctipo_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='STK_CBODEGA',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='BODEGA'),
        ),
    ]
