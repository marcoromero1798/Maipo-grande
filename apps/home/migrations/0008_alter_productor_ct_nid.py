# Generated by Django 3.2.6 on 2022-08-27 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20220827_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productor',
            name='CT_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CONTRATO', to='home.contrato'),
        ),
    ]