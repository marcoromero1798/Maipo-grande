# Generated by Django 3.2.6 on 2022-08-27 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_auto_20220827_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente_externo',
            name='US_NID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CLI_EXTERNO', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cliente_interno',
            name='US_NID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CLI_INTERNO', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='consultor',
            name='US_NID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CONSULTOR', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productor',
            name='US_NID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_PRODUCTOR', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transportista',
            name='US_NID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_TRANSPORTISTA', to=settings.AUTH_USER_MODEL),
        ),
    ]
