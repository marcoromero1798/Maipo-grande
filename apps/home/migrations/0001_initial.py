# Generated by Django 4.1 on 2022-11-27 22:16

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
                ('CP_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('CP_FOTO', models.ImageField(upload_to='images')),
            ],
            options={
                'db_table': 'CATEGORIA_PRODUCTO',
            },
        ),
        migrations.CreateModel(
            name='DESPACHO',
            fields=[
                ('DE_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID DESPACHO')),
                ('DE_CESTADO', models.CharField(blank=True, max_length=32, null=True, verbose_name='ESTADO')),
                ('DE_FFECHA_CREACION', models.DateTimeField(verbose_name='FECHA CREACION')),
                ('DE_FFECHA_ENTREGA', models.DateTimeField(verbose_name='FECHA ENTREGA')),
                ('DE_NPROCESADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='HABILITADO')),
            ],
            options={
                'db_table': 'DESPACHO',
            },
        ),
        migrations.CreateModel(
            name='DIRECCION',
            fields=[
                ('DR_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id Direccion')),
                ('DR_CNOMBRE', models.CharField(max_length=1024, verbose_name='Nombre')),
                ('DR_CCALLE', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Calle')),
                ('DR_CNUMERO', models.CharField(blank=True, max_length=32, null=True, verbose_name='Numero')),
                ('DR_CTELEFONO1', models.CharField(max_length=32, verbose_name='Telefono 1 ')),
                ('DR_CTELEFONO2', models.CharField(max_length=32, verbose_name='Telefono 2 ')),
                ('DR_NHABILITADO', models.BooleanField(default=True, verbose_name='Habilitado')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Id Socio Negocio')),
            ],
            options={
                'db_table': 'DIRECCION',
            },
        ),
        migrations.CreateModel(
            name='ORDEN_VENTA',
            fields=[
                ('OV_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID ORDEN DE VENTA')),
                ('OV_CESTADO', models.CharField(blank=True, max_length=32, null=True, verbose_name='ESTADO')),
                ('OV_FFECHA_CREACION', models.DateTimeField(verbose_name='FECHA CREACION')),
                ('OV_FFECHA_PROCESAMIENTO', models.DateTimeField(blank=True, null=True, verbose_name='FECHA PROCESAMIENTO')),
                ('OV_NPROCESADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='HABILITADO')),
                ('OV_CTIPO_PROCESO', models.CharField(max_length=50, verbose_name='Tipo Documento')),
                ('OV_COBSERVACIONES', models.CharField(max_length=100, verbose_name='Observaciones')),
                ('DR_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.direccion', verbose_name='ID DIRECCION ORDEN DE VENTA')),
            ],
            options={
                'db_table': 'ORDEN_VENTA',
            },
        ),
        migrations.CreateModel(
            name='PRODUCTO',
            fields=[
                ('PC_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID PRODUCTO')),
                ('PC_CCODIGO_PROD', models.CharField(max_length=128, verbose_name='COD PRODUCTO')),
                ('PC_CDESCRIPCION', models.CharField(max_length=128, verbose_name='DESCRIPCION')),
                ('PC_NPESO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Cantidad unidad de venta')),
                ('PC_NPRECIO_REF', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='PRECIO REFERENCIA')),
                ('PC_CUNIDAD_PESO', models.CharField(max_length=128, verbose_name='UNIDAD PESO')),
                ('PC_NCALIDAD', models.IntegerField(verbose_name='Dias Credito')),
                ('PC_CORIGEN', models.CharField(max_length=128, verbose_name='Origen')),
                ('PC_FOTO', models.ImageField(upload_to='images')),
                ('PC_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('PC_NREFRIGERACION', models.BooleanField(default=False, verbose_name='REFRIGERACION')),
                ('PC_FFECHA_VENCIMIENTO', models.DateTimeField(verbose_name='Fecha TERMINO')),
                ('CP_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='CATEGORIAPRODUCTO', to='home.categariaproducto')),
            ],
            options={
                'db_table': 'PRODUCTO',
            },
        ),
        migrations.CreateModel(
            name='SOLICITUD_COMPRA',
            fields=[
                ('SC_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID SOLICITUD')),
                ('SC_FFECHA_CREACION', models.DateTimeField(verbose_name='FECHA CREACION')),
                ('SC_FFECHA_PROCESAMIENTO', models.DateTimeField(blank=True, null=True, verbose_name='FECHA PROCESAMIENTO')),
                ('SC_NPROCESADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='Habilitado')),
                ('SC_CTIPO_SOLICITUD', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observaciones')),
                ('DR_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.direccion', verbose_name='ID DIRECCION SOLICITUD')),
            ],
            options={
                'db_table': 'SOLICITUD_COMPRA',
            },
        ),
        migrations.CreateModel(
            name='SUBASTA',
            fields=[
                ('SU_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID ORDEN DE VENTA SUBASTA')),
                ('SU_FFECHA_INICIO', models.DateTimeField(blank=True, null=True, verbose_name='FECHA INICIO')),
                ('SU_FFECHA_TERMINO', models.DateTimeField(blank=True, null=True, verbose_name='FECHA TERMINO')),
                ('SU_PESO_TOTAL', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='PRECIO')),
                ('SU_NREFRIGERACION', models.BooleanField(blank=True, default=False, null=True, verbose_name='REFRIGERACION')),
                ('SU_NPROCESADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='HABILITADO')),
                ('SU_NESTADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='HABILITADO')),
                ('DR_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.direccion', verbose_name='ID DIRECCION SUBASTA')),
                ('SU_NDOCUMENTO_ORIGEN', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.orden_venta', verbose_name='Documento origen')),
            ],
            options={
                'db_table': 'SUBASTA',
            },
        ),
        migrations.CreateModel(
            name='TIPO_CAMBIO',
            fields=[
                ('TC_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID ORDEN DE VENTA')),
                ('TC_CMONEDA', models.CharField(blank=True, max_length=32, null=True, verbose_name='Numero')),
                ('TC_NCONVERSION', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='CONVERSION')),
            ],
            options={
                'db_table': 'TIPO_CAMBIO',
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
                ('UX_CCORREO', models.CharField(max_length=128, null=True, verbose_name='Correo')),
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
                ('TR_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_TRANSPORTISTA', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'TRANSPORTISTA',
            },
        ),
        migrations.CreateModel(
            name='TRANSPORTE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TRA_NCARGA', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='CARGA TOTAL')),
                ('TRA_NREFRIGERACION', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('TRA_CMARCA', models.CharField(max_length=128, verbose_name='MARCA')),
                ('TRA_CMODELO', models.CharField(max_length=128, verbose_name='MODELO')),
                ('TRA_CPATENTE', models.CharField(max_length=128, verbose_name='PATENTE')),
                ('TRA_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('TR_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.transportista', verbose_name='USUARIO_TRANSPORTISTA')),
            ],
            options={
                'db_table': 'TRANSPORTE',
            },
        ),
        migrations.CreateModel(
            name='SUBASTA_DETALLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SUD_NCOBRO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='PRECIO')),
                ('SUD_NSELECCION', models.BooleanField(blank=True, default=False, null=True, verbose_name='Seleccion')),
                ('SU_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.subasta', verbose_name='ID SUBASTA')),
                ('TRA_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.transporte', verbose_name='ID TRANSPORTE')),
                ('TR_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.transportista', verbose_name='ID DIRECCION SUBASTA')),
            ],
            options={
                'db_table': 'SUBASTA_DETALLE',
            },
        ),
        migrations.AddField(
            model_name='subasta',
            name='SU_NTRANSPORTE_SELECCIONADO',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.transporte', verbose_name='Documento origen'),
        ),
        migrations.AddField(
            model_name='subasta',
            name='US_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ID DIRECCION SUBASTA'),
        ),
        migrations.CreateModel(
            name='STOCK',
            fields=[
                ('STK_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('STK_NQTY', models.IntegerField(verbose_name='Valor Transacción')),
                ('STK_CBODEGA', models.CharField(blank=True, max_length=100, null=True, verbose_name='BODEGA')),
                ('PC_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.producto', verbose_name='ID Item')),
            ],
            options={
                'db_table': 'STOCK',
            },
        ),
        migrations.CreateModel(
            name='SOLICITUD_COMPRA_DETALLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SC_NLINEA', models.IntegerField(verbose_name='Numero De Linea')),
                ('SCD_NQTY', models.IntegerField(verbose_name='CANTIDAD')),
                ('SCD_NPRECIO', models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='PRECIO')),
                ('SCD_NMONTO', models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='MONTO TOTAL')),
                ('SCD_NESTADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='Habilitado')),
                ('CP_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.categariaproducto', verbose_name='CATEGORIA PRODUCTO')),
                ('PC_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.producto', verbose_name='ID PRODUCTO SCD')),
                ('SC_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.solicitud_compra', verbose_name='ID SOLICITUD DETALLE')),
            ],
            options={
                'db_table': 'SOLICITUD_COMPRA_DETALLE',
            },
        ),
        migrations.AddField(
            model_name='solicitud_compra',
            name='TC_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.tipo_cambio', verbose_name='ID TIPO CAMBIO SOLICITUD'),
        ),
        migrations.AddField(
            model_name='solicitud_compra',
            name='US_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ID USUARIO SOLICITUD'),
        ),
        migrations.CreateModel(
            name='PRODUCTOR',
            fields=[
                ('PR_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Bodega')),
                ('PR_CDESCRIPCION', models.CharField(max_length=128, verbose_name='COD PRODUCTO')),
                ('PR_CCORREO', models.CharField(max_length=128, verbose_name='DESCRIPCION')),
                ('PR_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('PR_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_PRODUCTOR', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PRODUCTOR',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='PR_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FK_PRODUCTOR', to='home.productor'),
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
        migrations.CreateModel(
            name='PAGO_CUENTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PCA_FFECHA', models.DateTimeField(blank=True, null=True, verbose_name='FECHA INICIO')),
                ('PCA_NPRECIO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='PRECIO')),
                ('PCA_NQTY', models.IntegerField(verbose_name='CANTIDAD')),
                ('PCA_OV_ORIGEN', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.orden_venta', verbose_name='Orden de venta')),
                ('US_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'db_table': 'PAGO_CUENTA',
            },
        ),
        migrations.CreateModel(
            name='PAGO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PA_OV_ORIGEN', models.IntegerField(blank=True, null=True, verbose_name='CANTIDAD')),
                ('PA_FFECHA', models.DateTimeField(blank=True, null=True, verbose_name='FECHA INICIO')),
                ('PA_NPAGADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='Seleccion')),
                ('PA_CCODIGO', models.CharField(blank=True, max_length=100, null=True, verbose_name='codigo')),
                ('US_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'db_table': 'PAGO',
            },
        ),
        migrations.CreateModel(
            name='ORDEN_VENTA_DETALLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OVD_NQTY', models.IntegerField(verbose_name='CANTIDAD')),
                ('OVD_NLINEA', models.IntegerField(verbose_name='Numero De Linea')),
                ('OVD_NPRECIO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='PRECIO')),
                ('OVD_NMONTO', models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='MONTO TOTAL')),
                ('CP_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.categariaproducto', verbose_name='CATEGORIA PRODUCTO')),
                ('OV_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.orden_venta', verbose_name='ID SOLICITUD OVD')),
                ('PC_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.producto', verbose_name='ID PRODUCTO OVD')),
            ],
            options={
                'db_table': 'ORDEN_VENTA_DETALLE',
            },
        ),
        migrations.AddField(
            model_name='orden_venta',
            name='OV_NDOCUMENTO_ORIGEN',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.solicitud_compra', verbose_name='Documento origen'),
        ),
        migrations.AddField(
            model_name='orden_venta',
            name='TC_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.tipo_cambio', verbose_name='ID TIPO CAMBIO ORDEN DE VENTA'),
        ),
        migrations.AddField(
            model_name='orden_venta',
            name='US_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ID USUARIO ORDEN DE VENTA'),
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
                ('LG_CSECCION', models.CharField(max_length=128, verbose_name='SECCION')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_LOG', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'LOG_ACCIONES',
            },
        ),
        migrations.CreateModel(
            name='KARDEX',
            fields=[
                ('KX_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('KX_FFECHA_REGISTRO', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro')),
                ('KX_CTIPODOC', models.CharField(max_length=50, verbose_name='Tipo Documento')),
                ('KX_NNUMERDOC', models.BigIntegerField(verbose_name='Número Documento')),
                ('KX_FFECHADOC', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Documento')),
                ('KX_CES', models.CharField(max_length=50, verbose_name='E/S')),
                ('KX_NQTYTRANS', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Cantidad Transacción')),
                ('KX_NCOSTOTRANS', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Costo Transacción')),
                ('KX_NVALORTRANS', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Valor Transacción')),
                ('KX_NQTYACUM', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Cantidad Acumulada')),
                ('KX_NVALORACUM', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Valor Acumulado')),
                ('KX_NPRECIOPROMEDIO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='Precio Promedio')),
                ('KX_NDIA', models.BigIntegerField(verbose_name='DIA Documento')),
                ('KX_NMES', models.BigIntegerField(verbose_name='MES Documento')),
                ('KX_NAÑO', models.BigIntegerField(verbose_name='AÑO Documento')),
                ('PC_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.producto', verbose_name='ID Item')),
            ],
            options={
                'db_table': 'KARDEX',
            },
        ),
        migrations.CreateModel(
            name='DESPACHO_DETALLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DED_NQTY', models.IntegerField(verbose_name='CANTIDAD')),
                ('DED_NLINEA', models.IntegerField(verbose_name='Numero De Linea')),
                ('DED_NPRECIO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='PRECIO')),
                ('DED_NMONTO', models.DecimalField(decimal_places=5, max_digits=18, verbose_name='MONTO TOTAL')),
                ('DE_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.despacho', verbose_name='ID SOLICITUD DED')),
                ('PC_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.producto', verbose_name='ID PRODUCTO DED ')),
            ],
            options={
                'db_table': 'DESPACHO_DETALLE',
            },
        ),
        migrations.AddField(
            model_name='despacho',
            name='DR_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.direccion', verbose_name='ID DIRECCION DESPACHO'),
        ),
        migrations.AddField(
            model_name='despacho',
            name='TC_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.tipo_cambio', verbose_name='ID TIPO CAMBIO DESPACHO'),
        ),
        migrations.AddField(
            model_name='despacho',
            name='US_NID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ID USUARIO DESPACHO'),
        ),
        migrations.CreateModel(
            name='CONTRATO',
            fields=[
                ('CT_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Bodega')),
                ('CT_FFECHA_INICIO', models.DateTimeField(verbose_name='Fecha creacion')),
                ('CT_FFECHA_TERMINO', models.DateTimeField(verbose_name='Fecha creacion')),
                ('CT_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('PR_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_PRODUCTOR', to='home.productor')),
            ],
            options={
                'db_table': 'CONTRATO',
            },
        ),
        migrations.CreateModel(
            name='CONSULTOR',
            fields=[
                ('CON_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Cliente externo')),
                ('CON_CDESCRIPCION', models.CharField(max_length=128, verbose_name='Descripcion cliente')),
                ('CON_CCORREO', models.CharField(max_length=128, verbose_name='Correo')),
                ('CON_NCONTACTO', models.CharField(max_length=128, verbose_name='CONTACTO')),
                ('CON_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CONSULTOR', to=settings.AUTH_USER_MODEL)),
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
                ('CLI_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CLI_INTERNO', to=settings.AUTH_USER_MODEL)),
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
                ('CLE_NHABILITADO', models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado')),
                ('US_NID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='USUARIO_CLI_EXTERNO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CLIENTE_EXTERNO',
            },
        ),
        migrations.CreateModel(
            name='CARRO_COMPRA',
            fields=[
                ('CC_NID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID CARRO COMPRA')),
                ('CC_NQTY', models.IntegerField(verbose_name='CANTIDAD')),
                ('CC_NPRECIO', models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='PRECIO')),
                ('CC_NMONTO_TOTAL', models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='MONTO TOTAL')),
                ('CC_NESTADO', models.BooleanField(blank=True, default=False, null=True, verbose_name='ESTADO')),
                ('CP_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.categariaproducto', verbose_name='CATEGORIA PRODUCTO')),
                ('PC_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.producto', verbose_name='ID PRODUCTO CARRO COMPRA')),
                ('US_NID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ID USUARIO CARRO COMPRA')),
            ],
            options={
                'db_table': 'CARRO_COMPRA',
            },
        ),
    ]
