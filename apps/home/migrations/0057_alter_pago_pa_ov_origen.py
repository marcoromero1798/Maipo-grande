# Generated by Django 3.2.6 on 2022-11-11 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0056_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='PA_OV_ORIGEN',
            field=models.IntegerField(blank=True, null=True, verbose_name='CANTIDAD'),
        ),
    ]