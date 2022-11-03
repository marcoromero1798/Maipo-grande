# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from tabnanny import verbose
from tkinter import CASCADE, N
from tkinter.tix import Tree
from turtle import pos
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from pyparsing import null_debug_action
from core.sql import *
from datetime import date, datetime, timedelta ,timezone
# Create your models here.


class PARAMETRO(models.Model):
    PM_CGRUPO = models.CharField(("Grupo Parametro"),max_length=128,null=False)
    PM_CCODIGO = models.CharField(("Codigo Parametro"),max_length=128,null=False)
    PM_CDESCRIPCION = models.CharField(("Descripcion"),max_length=1024)
    PM_CVALOR1 = models.CharField(("Valor Texto 1"),max_length=1024)
    PM_CVALOR2 = models.CharField(("Valor Texto 2"),max_length=1024)
    PM_CVALOR3 = models.CharField(("Valor Texto 3"),max_length=1024)
    PM_NVALOR1 = models.DecimalField(("Valor Numerico 1"),max_digits=18,decimal_places=5)
    PM_NVALOR2 = models.DecimalField(("Valor Numerico 2"),max_digits=18,decimal_places=5)
    PM_NVALOR3 = models.DecimalField(("Valor Numerico 3"),max_digits=18,decimal_places=5)

    class Meta:
        db_table = 'PARAMETRO'
        
        unique_together = (('PM_CGRUPO', 'PM_CCODIGO'),)

    def __str__(self):
        return self.PM_CCODIGO
class TIPO_CAMBIO(models.Model):
    TC_NID = models.BigAutoField(("ID ORDEN DE VENTA"),primary_key=True)
    TC_CMONEDA = models.CharField(("Numero"),max_length=32,null=True,blank=True)
    TC_NCONVERSION = models.DecimalField(("CONVERSION"),max_digits=18,decimal_places=5)

    class Meta:
        db_table = 'TIPO_CAMBIO'


class DIRECCION(models.Model):
    DR_NID = models.BigAutoField(("Id Direccion"),primary_key=True)
    US_NID = models.ForeignKey(User,verbose_name="Id Socio Negocio",on_delete=models.PROTECT)
    DR_CNOMBRE = models.CharField(("Nombre"),max_length=1024)
    DR_CCALLE = models.CharField(("Calle"),max_length=1024,null=True,blank=True)
    DR_CNUMERO = models.CharField(("Numero"),max_length=32,null=True,blank=True)
    DR_CTELEFONO1 = models.CharField(("Telefono 1 "),max_length=32)
    DR_CTELEFONO2 = models.CharField(("Telefono 2 "),max_length=32)
    DR_NHABILITADO = models.BooleanField(("Habilitado"),default=True)

    class Meta:
        db_table = 'DIRECCION'

class CATEGARIAPRODUCTO(models.Model):
    CP_NID = models.BigAutoField(("ID CATEGORIA"),primary_key=True)
    CP_CDESCRIPCION = models.CharField(("DESCRIPCION "),max_length=128)
    CP_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    CP_FOTO = models.ImageField(upload_to="images")


    class Meta:
        db_table = 'CATEGORIA_PRODUCTO'

    def __str__(self):
        return self.CP_CDESCRIPCION
class USERS_EXTENSION(models.Model):
    US_NID = models.OneToOneField(User, related_name='USER', on_delete=models.PROTECT)
    UX_CTELEFONO = models.CharField(("Telefono"),max_length=128)
    UX_CTELEGRAM_ID = models.CharField(("ID Telegram"),max_length=128,null=True,blank=True)
    UX_CTELEGRAM_USER = models.CharField(("Usuario Telegram"),max_length=128,null=True,blank=True)
    UX_CRUT = models.CharField(("Rut"),max_length=16)
    UX_NHABILITADO = models.BooleanField(("Habilitado"))
    UX_IS_ADMINISTRADOR = models.BooleanField(default=False)
    UX_IS_TRANSPORTISTA = models.BooleanField(default=False)
    UX_IS_CLIENTEEXTERNO = models.BooleanField(default=False)
    UX_IS_CLIENTEINTERNO = models.BooleanField(default=False)
    UX_IS_CONSULTOR = models.BooleanField(default=False)
    UX_IS_PRODUCTOR = models.BooleanField(default=False)

    class Meta:
        db_table = 'USERS_EXTENSION'

    def __str__(self):
        return self.UX_CRUT

class PRODUCTOR(models.Model):
    PR_NID = models.BigAutoField(("ID Bodega"),primary_key=True)
    PR_CDESCRIPCION = models.CharField(("COD PRODUCTO"),max_length=128)
    PR_CCORREO = models.CharField(("DESCRIPCION"),max_length=128)
    PR_NCONTACTO = models.CharField(("CONTACTO"),max_length=128)
    PR_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_PRODUCTOR', on_delete=models.PROTECT)
    class Meta:
        db_table = 'PRODUCTOR'

    def __str__(self):
        return self.PR_CDESCRIPCION

class CONTRATO(models.Model):
    CT_NID = models.BigAutoField(("ID Bodega"),primary_key=True)
    CT_FFECHA_INICIO = models.DateTimeField(("Fecha creacion"))
    CT_FFECHA_TERMINO = models.DateTimeField(("Fecha creacion"))
    CT_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    PR_NID = models.ForeignKey(PRODUCTOR, related_name='USUARIO_PRODUCTOR', on_delete=models.PROTECT)
    class Meta:
        db_table = 'CONTRATO'

    def __str__(self):
        return str(self.CT_NID)
class PRODUCTO(models.Model):
    PC_NID = models.BigAutoField(("ID PRODUCTO"),primary_key=True)
    PC_CCODIGO_PROD = models.CharField(("COD PRODUCTO"),max_length=128)
    PC_CDESCRIPCION = models.CharField(("DESCRIPCION"),max_length=128)
    PC_NPESO = models.DecimalField(("Cantidad unidad de venta"),max_digits=18,decimal_places=5)
    PC_NPRECIO_REF = models.DecimalField(("PRECIO REFERENCIA"),max_digits=18,decimal_places=5)
    PC_CUNIDAD_PESO = models.CharField(("UNIDAD PESO"),max_length=128)
    PC_NCALIDAD = models.IntegerField(('Dias Credito'))
    PC_CORIGEN = models.CharField(("Origen"),max_length=128)
    PC_FOTO = models.ImageField( upload_to="images")
    PC_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    PC_NREFRIGERACION = models.BooleanField(("REFRIGERACION"),default=False)
    PR_NID = models.ForeignKey(PRODUCTOR, related_name='FK_PRODUCTOR', on_delete=models.PROTECT,null=True,blank=True)
    CP_NID = models.ForeignKey(CATEGARIAPRODUCTO, related_name='CATEGORIAPRODUCTO', on_delete=models.PROTECT)
    PC_FFECHA_VENCIMIENTO = models.DateTimeField(("Fecha TERMINO"))
    class Meta:
        db_table = 'PRODUCTO'

    def __str__(self):
        return self.PC_CDESCRIPCION

class CLIENTE_EXTERNO(models.Model):
    CLE_NID = models.BigAutoField(("ID Cliente externo"),primary_key=True)
    CLE_CDESCRIPCION = models.CharField(("Descripcion cliente"),max_length=128)
    CLE_CCORREO = models.CharField(("Correo"),max_length=128)
    CLE_NCONTACTO = models.CharField(("CONTACTO"),max_length=128)
    CLE_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_CLI_EXTERNO', on_delete=models.PROTECT)
    class Meta:
        db_table = 'CLIENTE_EXTERNO'

    def __str__(self):
        return self.CLE_CDESCRIPCION
class CLIENTE_INTERNO(models.Model):
    CLI_NID = models.BigAutoField(("ID Cliente externo"),primary_key=True)
    CLI_CDESCRIPCION = models.CharField(("Descripcion cliente"),max_length=128)
    CLI_CCORREO = models.CharField(("Correo"),max_length=128)
    CLI_NCONTACTO = models.CharField(("CONTACTO"),max_length=128)
    CLI_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_CLI_INTERNO', on_delete=models.PROTECT)
    class Meta:
        db_table = 'CLIENTE_INTERNO'

    def __str__(self):
        return self.CLI_CDESCRIPCION
class CONSULTOR(models.Model):
    CON_NID = models.BigAutoField(("ID Cliente externo"),primary_key=True)
    CON_CDESCRIPCION = models.CharField(("Descripcion cliente"),max_length=128)
    CON_CCORREO = models.CharField(("Correo"),max_length=128)
    CON_NCONTACTO = models.CharField(("CONTACTO"),max_length=128)
    CON_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_CONSULTOR', on_delete=models.PROTECT)
    class Meta:
        db_table = 'CONSULTOR'

    def __str__(self):
        return self.CON_CDESCRIPCION
class TRANSPORTISTA(models.Model):
    TR_NID = models.BigAutoField(("ID Cliente externo"),primary_key=True)
    TR_CDESCRIPCION = models.CharField(("Descripcion cliente"),max_length=128)
    TR_CCORREO = models.CharField(("Correo"),max_length=128)
    TR_NCONTACTO = models.CharField(("CONTACTO"),max_length=128)
    TR_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_TRANSPORTISTA', on_delete=models.PROTECT)
    class Meta:
        db_table = 'TRANSPORTISTA'

    def __str__(self):
        return self.TR_CDESCRIPCION
class TRANSPORTE(models.Model):
    TR_NID = models.ForeignKey(TRANSPORTISTA, verbose_name='USUARIO_TRANSPORTISTA', on_delete=models.PROTECT,null=True,blank=True)
    TRA_NCARGA = models.DecimalField(("CARGA TOTAL"),max_digits=18,decimal_places=5)
    TRA_NREFRIGERACION = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    TRA_CMARCA = models.CharField(("MARCA"),max_length=128)  
    TRA_CMODELO = models.CharField(("MODELO"),max_length=128)  
    TRA_CPATENTE = models.CharField(("PATENTE"),max_length=128) 
    TRA_NHABILITADO= models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    class Meta:
        db_table = 'TRANSPORTE'

    def __str__(self):
        DESCRIPCION = self.TRA_CMARCA +' '+self.TRA_CMODELO+' '+self.TRA_CMODELO 
        return str(DESCRIPCION)
        
class LOG_ACCIONES(models.Model):
    LG_NID = models.BigAutoField(("ID"),primary_key=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_LOG', on_delete=models.PROTECT)
    LG_CACCION = models.CharField(("ACCION"),max_length=128)
    LG_FFECHA_ACCION = models.DateTimeField(("Fecha creacion"))
    LG_CMODULO = models.CharField(("MODULO"),max_length=128)
    LG_CSECCION = models.CharField(("SECCION"),max_length=128)
    class Meta:
        db_table = 'LOG_ACCIONES'

    def __str__(self):
        return str(self.LG_NID)
class LOG_PRO(models.Model):
    LGP_NID = models.BigAutoField(("ID"),primary_key=True)
    US_NID = models.ForeignKey(User, related_name='USUARIO_PROCESO', on_delete=models.PROTECT)
    LGP_CACCION = models.CharField(("ACCION"),max_length=128)
    LGP_CESTADO = models.CharField(("ESTADO"),max_length=128)
    LGP_FFECHA_CREACION = models.DateTimeField(("Fecha CREACION"))
    LGP_FFECHA_INICIO = models.DateTimeField(("Fecha INICIO"))
    LGP_FFECHA_TERMINO = models.DateTimeField(("Fecha TERMINO"))
    class Meta:
        db_table = 'LOG_PROCESO'

    def __str__(self):
        return str(self.LGP_NID)



class DESPACHO(models.Model):
    DE_NID = models.BigAutoField(("ID DESPACHO"),primary_key=True)
    US_NID = models.ForeignKey(User, verbose_name='ID USUARIO DESPACHO', on_delete=models.PROTECT,null = True,blank =True)
    DR_NID = models.ForeignKey(DIRECCION, verbose_name='ID DIRECCION DESPACHO', on_delete=models.PROTECT,null = True,blank =True)
    TC_NID = models.ForeignKey(TIPO_CAMBIO, verbose_name='ID TIPO CAMBIO DESPACHO', on_delete=models.PROTECT,null = True,blank =True)
    DE_CESTADO = models.CharField(("ESTADO"),max_length=32,null=True,blank=True)
    DE_FFECHA_CREACION = models.DateTimeField(("FECHA CREACION"))
    DE_FFECHA_ENTREGA = models.DateTimeField(("FECHA ENTREGA"))
    DE_NPROCESADO = models.BooleanField(("HABILITADO"),default=False,null=True,blank=True)    
    
    class Meta:
        db_table = 'DESPACHO'

    def __str__(self):
        return str(self.DE_NID)

class DESPACHO_DETALLE(models.Model):
    DE_NID = models.ForeignKey(DESPACHO, verbose_name='ID SOLICITUD DED', on_delete=models.PROTECT)
    PC_NID = models.ForeignKey(PRODUCTO, verbose_name='ID PRODUCTO DED ', on_delete=models.PROTECT)
    DED_NQTY = models.IntegerField(("CANTIDAD"))
    DED_NLINEA = models.IntegerField(("Numero De Linea"))
    DED_NPRECIO = models.DecimalField(("PRECIO"),max_digits=18,decimal_places=5)
    DED_NMONTO = models.DecimalField(("MONTO TOTAL"),max_digits=18,decimal_places=5)   

    class Meta:
        db_table = 'DESPACHO_DETALLE'

    def __str__(self):
        return str(self.DE_NID)

class CARRO_COMPRA(models.Model):
    CC_NID = models.BigAutoField(("ID CARRO COMPRA"),primary_key=True)
    US_NID = models.ForeignKey(User, verbose_name='ID USUARIO CARRO COMPRA', on_delete=models.PROTECT,null = True,blank =True)
    PC_NID = models.ForeignKey(PRODUCTO, verbose_name='ID PRODUCTO CARRO COMPRA', on_delete=models.PROTECT,null = True,blank =True)
    CP_NID = models.ForeignKey(CATEGARIAPRODUCTO, verbose_name='CATEGORIA PRODUCTO', on_delete=models.PROTECT,null = True,blank =True)
    CC_NQTY = models.IntegerField(("CANTIDAD"))
    CC_NPRECIO = models.DecimalField(("PRECIO"),max_digits=18,decimal_places=5,null=True,blank=True)   
    CC_NMONTO_TOTAL = models.DecimalField(("MONTO TOTAL"),max_digits=18,decimal_places=5,null=True,blank=True)   
    CC_NESTADO = models.BooleanField(("ESTADO"),default=False,null=True,blank=True)

    class Meta:
        db_table = 'CARRO_COMPRA'

    def __str__(self):
        return str(self.CC_NID)



class KARDEX(models.Model):
    KX_NID = models.BigAutoField(("ID"), primary_key=True)
    PC_NID = models.ForeignKey(PRODUCTO,verbose_name="ID Item",on_delete=models.PROTECT)
    KX_FFECHA_REGISTRO = models.DateTimeField(("Fecha Registro"),auto_now_add=True)
    KX_CTIPODOC  = models.CharField(("Tipo Documento"),max_length=50)
    KX_NNUMERDOC = models.BigIntegerField(("Número Documento"))
    KX_FFECHADOC = models.DateTimeField(("Fecha Documento"),auto_now_add=True)
    KX_CES  = models.CharField(("E/S"),max_length=50)
    KX_NQTYTRANS = models.DecimalField(("Cantidad Transacción"),max_digits=18,decimal_places=5)
    KX_NCOSTOTRANS = models.DecimalField(("Costo Transacción"),max_digits=18,decimal_places=5)
    KX_NVALORTRANS = models.DecimalField(("Valor Transacción"),max_digits=18,decimal_places=5)
    KX_NQTYACUM = models.DecimalField(("Cantidad Acumulada"),max_digits=18,decimal_places=5)
    KX_NVALORACUM = models.DecimalField(("Valor Acumulado"),max_digits=18,decimal_places=5)
    KX_NPRECIOPROMEDIO = models.DecimalField(("Precio Promedio"),max_digits=18,decimal_places=5)
    KX_NDIA = models.BigIntegerField(("DIA Documento"))
    KX_NMES = models.BigIntegerField(("MES Documento"))
    KX_NAÑO = models.BigIntegerField(("AÑO Documento"))
    

    class Meta:
        db_table = "KARDEX"
    
    def __str__(self):
        return str(self.KX_NID)

class STOCK(models.Model):
    STK_NID = models.BigAutoField(("ID"), primary_key=True) 
    PC_NID = models.ForeignKey(PRODUCTO,verbose_name="ID Item",on_delete=models.PROTECT)
    STK_NQTY = models.IntegerField(("Valor Transacción"))

    class Meta:
        db_table = "STOCK"
    
    def __str__(self):
        return str(self.STK_NQTY)

####################
# TRANSACCIONALES  #
####################
class SOLICITUD_COMPRA(models.Model):
    SC_NID = models.BigAutoField(("ID SOLICITUD"),primary_key=True)
    US_NID = models.ForeignKey(User, verbose_name='ID USUARIO SOLICITUD', on_delete=models.PROTECT,null = True,blank =True)
    DR_NID = models.ForeignKey(DIRECCION, verbose_name='ID DIRECCION SOLICITUD', on_delete=models.PROTECT,null = True,blank =True)
    TC_NID = models.ForeignKey(TIPO_CAMBIO, verbose_name='ID TIPO CAMBIO SOLICITUD', on_delete=models.PROTECT,null = True,blank =True)
    SC_FFECHA_CREACION = models.DateTimeField(("FECHA CREACION"))
    SC_FFECHA_PROCESAMIENTO = models.DateTimeField(("FECHA PROCESAMIENTO"),null=True,blank=True)
    SC_NPROCESADO = models.BooleanField(("Habilitado"),default=False,null=True,blank=True)
    # SCD_NMONTO_TOTAL = models.DecimalField(("MONTO TOTAL"),max_digits=18,decimal_places=5)   

    class Meta:
        db_table = 'SOLICITUD_COMPRA'
    def __str__(self):
        return str(self.SC_NID)
class SOLICITUD_COMPRA_DETALLE(models.Model):
    SC_NID = models.ForeignKey(SOLICITUD_COMPRA, verbose_name='ID SOLICITUD DETALLE', on_delete=models.PROTECT)
    SC_NLINEA = models.IntegerField(("Numero De Linea"))
    PC_NID = models.ForeignKey(PRODUCTO, verbose_name='ID PRODUCTO SCD', on_delete=models.PROTECT,null = True,blank =True)
    CP_NID = models.ForeignKey(CATEGARIAPRODUCTO, verbose_name='CATEGORIA PRODUCTO', on_delete=models.PROTECT,null = True,blank =True)
    SCD_NQTY = models.IntegerField(("CANTIDAD"))
    SCD_NPRECIO = models.DecimalField(("PRECIO"),max_digits=18,decimal_places=5,null = True,blank =True)
    SCD_NMONTO = models.DecimalField(("MONTO TOTAL"),max_digits=18,decimal_places=5,null = True,blank =True)   
    SCD_NESTADO = models.BooleanField(("Habilitado"),default=False,null=True,blank=True)

    class Meta:
        db_table = 'SOLICITUD_COMPRA_DETALLE'
    
    @property
    def ESTADO_PEDIDO(self):
        qty_sc = detalle_solicitud(self.CP_NID_id,self.SC_NID_id)
        qty_ov = detalle_ov(self.CP_NID_id,self.SC_NID_id)
        if (qty_sc -qty_ov )  == 0:
            return 'COMPLETADO'
        else:
            return 'PENDIENTE'
    def __str__(self):
        return str(self.SC_NID)

class ORDEN_VENTA(models.Model):
    OV_NID = models.BigAutoField(("ID ORDEN DE VENTA"),primary_key=True)
    OV_NDOCUMENTO_ORIGEN = models.ForeignKey(SOLICITUD_COMPRA,on_delete=models.PROTECT,verbose_name="Documento origen",null = True,blank =True)
    US_NID = models.ForeignKey(User, verbose_name='ID USUARIO ORDEN DE VENTA', on_delete=models.PROTECT,null = True,blank =True)
    DR_NID = models.ForeignKey(DIRECCION, verbose_name='ID DIRECCION ORDEN DE VENTA', on_delete=models.PROTECT,null = True,blank =True)
    TC_NID = models.ForeignKey(TIPO_CAMBIO, verbose_name='ID TIPO CAMBIO ORDEN DE VENTA', on_delete=models.PROTECT,null = True,blank =True)
    OV_CESTADO = models.CharField(("ESTADO"),max_length=32,null=True,blank=True)
    OV_FFECHA_CREACION = models.DateTimeField(("FECHA CREACION"))
    OV_FFECHA_PROCESAMIENTO = models.DateTimeField(("FECHA PROCESAMIENTO"),null=True,blank=True)
    OV_NPROCESADO = models.BooleanField(("HABILITADO"),default=False,null=True,blank=True)    
    OV_CTIPO_PROCESO = models.CharField(("Tipo Documento"),max_length=50)
    OV_COBSERVACIONES = models.CharField(("Observaciones"),max_length=100)
    
    class Meta:
        db_table = 'ORDEN_VENTA'

    def __str__(self):
        return str(self.OV_NID)

class ORDEN_VENTA_DETALLE(models.Model):
    OV_NID = models.ForeignKey(ORDEN_VENTA, verbose_name='ID SOLICITUD OVD', on_delete=models.PROTECT,blank=True,null =True)
    PC_NID = models.ForeignKey(PRODUCTO, verbose_name='ID PRODUCTO OVD', on_delete=models.PROTECT)
    CP_NID = models.ForeignKey(CATEGARIAPRODUCTO, verbose_name='CATEGORIA PRODUCTO', on_delete=models.PROTECT,null = True,blank =True)
    OVD_NQTY = models.IntegerField(("CANTIDAD"))
    OVD_NLINEA = models.IntegerField(("Numero De Linea"))
    OVD_NPRECIO = models.DecimalField(("PRECIO"),max_digits=18,decimal_places=5)
    OVD_NMONTO = models.DecimalField(("MONTO TOTAL"),max_digits=18,decimal_places=5,null = True,blank =True)   
    class Meta:
        db_table = 'ORDEN_VENTA_DETALLE'
    def __str__(self):
        return str(self.OV_NID)
    @property
    def MONTO_TOTAL(self):
        return self.OVD_NPRECIO * self.OVD_NQTY
    @property
    def IVA(self):
        return (self.OVD_NPRECIO * self.OVD_NQTY) * 0,19
    @property
    def TOTAL_IVA(self):
        return (self.OVD_NPRECIO * self.OVD_NQTY) * 1,19


class SUBASTA(models.Model):
    SU_NID =  models.BigAutoField(("ID ORDEN DE VENTA SUBASTA"),primary_key=True)
    US_NID = models.ForeignKey(User, verbose_name='ID DIRECCION SUBASTA', on_delete=models.PROTECT,null = True,blank =True)
    DR_NID = models.ForeignKey(DIRECCION, verbose_name='ID DIRECCION SUBASTA', on_delete=models.PROTECT,null = True,blank =True)
    SU_NDOCUMENTO_ORIGEN = models.ForeignKey(ORDEN_VENTA,on_delete=models.PROTECT,verbose_name="Documento origen",null = True,blank =True)
    SU_FFECHA_INICIO = models.DateTimeField(("FECHA INICIO"),null=True,blank=True) 
    SU_FFECHA_TERMINO = models.DateTimeField(("FECHA TERMINO"),null=True,blank=True)
    SU_PESO_TOTAL = models.DecimalField(("PRECIO"),max_digits=18,decimal_places=5) 
    SU_NREFRIGERACION = models.BooleanField(("REFRIGERACION"),default=False,null=True,blank=True)
    SU_NPROCESADO = models.BooleanField(("HABILITADO"),default=False,null=True,blank=True)    
    SU_NESTADO = models.BooleanField(("HABILITADO"),default=False,null=True,blank=True)    
    SU_NTRANSPORTE_SELECCIONADO= models.ForeignKey(TRANSPORTE,on_delete=models.PROTECT,verbose_name="Documento origen",null = True,blank =True)
    class Meta:
        db_table = 'SUBASTA'

    @property
    def VIGENCIA(self):
        fecha_consulta = datetime.now(self.SU_FFECHA_TERMINO.tzinfo)
        if self.SU_FFECHA_TERMINO != None:
            fecha_termino = self.SU_FFECHA_TERMINO
            if fecha_consulta >= fecha_termino:
                return 'TERMINADA'
            else:
                return 'VIGENTE'
        else:
            return 'NO INICIADA'

    def __str__(self):
        return str(self.SU_NID)
class SUBASTA_DETALLE(models.Model):
    SU_NID = models.ForeignKey(SUBASTA, verbose_name='ID SUBASTA', on_delete=models.PROTECT,null = True,blank =True)
    TRA_NID = models.ForeignKey(TRANSPORTE, verbose_name='ID TRANSPORTE', on_delete=models.PROTECT,null = True,blank =True)
    TR_NID = models.ForeignKey(TRANSPORTISTA, verbose_name='ID DIRECCION SUBASTA', on_delete=models.PROTECT,null = True,blank =True)
    SUD_NCOBRO = models.DecimalField(("PRECIO"),max_digits=18,decimal_places=5) 
    SUD_NSELECCION =  models.BooleanField(("Seleccion"),default=False,null=True,blank=True)    
    class Meta:
        db_table = 'SUBASTA_DETALLE'