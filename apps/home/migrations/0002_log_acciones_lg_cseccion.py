# Generated by Django 3.2.6 on 2022-08-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log_acciones',
            name='LG_CSECCION',
            field=models.CharField(default=1, max_length=128, verbose_name='SECCION'),
            preserve_default=False,
        ),
    ]
