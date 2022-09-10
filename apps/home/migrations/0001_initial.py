# Generated by Django 3.2.6 on 2022-08-27 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CATEGARIAPRODUCTO',
            fields=[
                ('CP_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID CATEGORIA')),
                ('CP_CDESCRIPCION', models.CharField(max_length=128, verbose_name='DESCRIPCION ')),
            ],
            options={
                'db_table': 'CATEGORIA_PRODUCTO',
            },
        ),
        migrations.CreateModel(
            name='CONTRATO',
            fields=[
                ('CT_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Bodega')),
                ('CT_FFECHA_INICIO', models.DateTimeField(verbose_name='Fecha creacion')),
                ('CT_FFECHA_TERMINO', models.DateTimeField(verbose_name='Fecha creacion')),
                ('CT_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
            ],
            options={
                'db_table': 'CONTRATO',
            },
        ),
        migrations.CreateModel(
            name='USERS_EXTENSION',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UX_CTELEFONO', models.CharField(max_length=128, verbose_name='Telefono')),
                ('UX_CTELEGRAM_ID', models.CharField(blank=True, max_length=128, null=True, verbose_name='ID Telegram')),
                ('UX_CTELEGRAM_USER', models.CharField(blank=True, max_length=128, null=True, verbose_name='Usuario Telegram')),
                ('UX_CRUT', models.CharField(max_length=16, verbose_name='Rut')),
                ('UX_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('UX_IS_ADMINISTRADOR', models.BooleanField(default=False)),
                ('UX_IS_TRANSPORTISTA', models.BooleanField(default=False)),
                ('UX_IS_CLIENTEEXTERNO', models.BooleanField(default=False)),
                ('UX_IS_CLIENTEINTERNO', models.BooleanField(default=False)),
                ('UX_IS_CONSULTOR', models.BooleanField(default=False)),
                ('UX_IS_PRODUCTOR', models.BooleanField(default=False)),
                ('US_NID', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'USERS_EXTENSION',
            },
        ),
        migrations.CreateModel(
            name='TRANSPORTISTA',
            fields=[
                ('TR_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Cliente externo')),
                ('TR_CDESCRIPCION', models.CharField(max_length=128, verbose_name='Descripcion cliente')),
                ('TR_CCORREO', models.CharField(max_length=128, verbose_name='Correo')),
                ('TR_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('TR_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('US_NID', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_TRANSPORTISTA', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'TRANSPORTISTA',
            },
        ),
        migrations.CreateModel(
            name='PRODUCTOR',
            fields=[
                ('PR_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Bodega')),
                ('PR_CDESCRIPCION', models.CharField(max_length=128, verbose_name='COD PRODUCTO')),
                ('PR_CCORREO', models.CharField(max_length=128, verbose_name='DESCRIPCION')),
                ('PR_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('PR_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('CT_NID', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CONTRATO', to='home.contrato')),
                ('US_NID', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_PRODUCTOR', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PRODUCTOR',
            },
        ),
        migrations.CreateModel(
            name='PRODUCTO',
            fields=[
                ('PC_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID PRODUCTO')),
                ('PC_CCODIGO_PROD', models.CharField(max_length=128, verbose_name='COD PRODUCTO')),
                ('PC_CDESCRIPCION', models.CharField(max_length=128, verbose_name='DESCRIPCION')),
                ('PC_NPRECIO', models.IntegerField(verbose_name='Precio')),
                ('PC_NCALIDAD', models.IntegerField(verbose_name='Calidad')),
                ('PC_CORIGEN', models.CharField(max_length=128,verbose_name='Origen')),
                ('PC_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('CP_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CATEGORIAPRODUCTO', to='home.categariaproducto')),
                ('PR_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FK_PRODUCTOR', to='home.productor')),
            ],
            options={
                'db_table': 'PRODUCTO',
            },
        ),
        migrations.CreateModel(
            name='LOG_PRO',
            fields=[
                ('LGP_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('LGP_CACCION', models.CharField(max_length=128, verbose_name='ACCION')),
                ('LGP_CESTADO', models.CharField(max_length=128, verbose_name='ESTADO')),
                ('LGP_FFECHA_CREACION', models.DateTimeField(verbose_name='Fecha CREACION')),
                ('LGP_FFECHA_INICIO', models.DateTimeField(verbose_name='Fecha INICIO')),
                ('LGP_FFECHA_TERMINO', models.DateTimeField(verbose_name='Fecha TERMINO')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_PROCESO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'LOG_PROCESO',
            },
        ),
        migrations.CreateModel(
            name='LOG_ACCIONES',
            fields=[
                ('LG_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('LG_CACCION', models.CharField(max_length=128, verbose_name='ACCION')),
                ('LG_FFECHA_ACCION', models.DateTimeField(verbose_name='Fecha creacion')),
                ('LG_CMODULO', models.CharField(max_length=128, verbose_name='MODULO')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_LOG', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'LOG_ACCIONES',
            },
        ),
        migrations.CreateModel(
            name='CONSULTOR',
            fields=[
                ('CON_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Cliente externo')),
                ('CON_CDESCRIPCION', models.CharField(max_length=128, verbose_name='Descripcion cliente')),
                ('CON_CCORREO', models.CharField(max_length=128, verbose_name='Correo')),
                ('CON_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('CON_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('US_NID', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CONSULTOR', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CONSULTOR',
            },
        ),
        migrations.CreateModel(
            name='CLIENTE_INTERNO',
            fields=[
                ('CLI_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Cliente externo')),
                ('CLI_CDESCRIPCION', models.CharField(max_length=128, verbose_name='Descripcion cliente')),
                ('CLI_CCORREO', models.CharField(max_length=128, verbose_name='Correo')),
                ('CLI_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('CLI_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('US_NID', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CLI_INTERNO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CLIENTE_INTERNO',
            },
        ),
        migrations.CreateModel(
            name='CLIENTE_EXTERNO',
            fields=[
                ('CLE_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Cliente externo')),
                ('CLE_CDESCRIPCION', models.CharField(max_length=128, verbose_name='Descripcion cliente')),
                ('CLE_CCORREO', models.CharField(max_length=128, verbose_name='Correo')),
                ('CLE_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('CLE_NHABILITADO', models.BooleanField(verbose_name='Habilitado')),
                ('US_NID', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CLI_EXTERNO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CLIENTE_EXTERNO',
            },
        ),
    ]
