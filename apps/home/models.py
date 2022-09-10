# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from tkinter import N
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
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


class CATEGARIAPRODUCTO(models.Model):
    CP_NID = models.BigAutoField(("ID CATEGORIA"),primary_key=True)
    CP_CDESCRIPCION = models.CharField(("DESCRIPCION "),max_length=128)
    CP_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)

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
    PC_NPRECIO = models.IntegerField(("Precio"))
    PC_NPESO = models.DecimalField(("Cantidad unidad de venta"),max_digits=18,decimal_places=5)
    PC_CUNIDAD_PESO = models.CharField(("UNIDAD PESO"),max_length=128)
    PC_NCALIDAD = models.IntegerField(('Dias Credito'))
    PC_CORIGEN = models.CharField(("Origen"),max_length=128)
    PC_NHABILITADO = models.BooleanField(("Habilitado"),default=True,null=True,blank=True)
    PR_NID = models.ForeignKey(PRODUCTOR, related_name='FK_PRODUCTOR', on_delete=models.PROTECT,null=True,blank=True)
    CP_NID = models.ForeignKey(CATEGARIAPRODUCTO, related_name='CATEGORIAPRODUCTO', on_delete=models.PROTECT,null=True,blank=True)
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
        return self.LG_NID
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
        return self.LGP_NID




