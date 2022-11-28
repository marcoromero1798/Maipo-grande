from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from core.sql import *
from apps.home.models import *
from django.contrib.auth.forms import UserCreationForm

class formCONTRATO(forms.ModelForm):
    class Meta:
        model = CONTRATO
        # CT_NID
        # CT_FFECHA_CREACION
        # CT_FFECHA_VIGENCIA
        # CT_NHABILITADO
	
        fields = [
        'CT_FFECHA_INICIO',
        'CT_FFECHA_TERMINO',
        'PR_NID'
        ]
        labels = '__all__'
        widgets = {        
            'CT_FFECHA_INICIO': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'form-control','type':'datetime-local'}),
            'CT_FFECHA_TERMINO' : forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'form-control','type':'datetime-local'}),
            'PR_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),

        }
class formCATEGORIA(forms.ModelForm):
    class Meta:
        model = CATEGARIAPRODUCTO
        # CT_NID
        # CT_FFECHA_CREACION
        # CT_FFECHA_VIGENCIA
        # CT_NHABILITADO
	
        fields = [
        'CP_CDESCRIPCION',

        ]
        labels = '__all__'
        widgets = {        
            'CP_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
           
        }
class formSTOCK(forms.ModelForm):
    class Meta:
        model = STOCK
        # CT_NID
        # CT_FFECHA_CREACION
        # CT_FFECHA_VIGENCIA
        # CT_NHABILITADO
	
        fields = [
        'PC_NID',
        'STK_NQTY',
        'STK_CBODEGA'

        ]
        labels = '__all__'
        widgets = {        
            'PC_NID': forms.Select(attrs={'class': 'form-control','type':'text'}),
            'STK_NQTY': forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1'}),
            'STK_CBODEGA' : forms.Select(choices=[('INTERNA','INTERNA'),('EXTERNA','EXTERNA')],attrs={'class': 'form-control','type':'text'}),

        }
class formPRODUCTOR(forms.ModelForm):
    class Meta:
        model = PRODUCTOR
        # PR_CDESCRIPCION
        # PR_CCORREO
        # PR_NCONTACTO
        # PR_NHABILITADO
        # US_NID
        # CT_NID
	
        fields = [
        'PR_CDESCRIPCION',
        'PR_CCORREO',
        'PR_NCONTACTO',
        'US_NID',


        ]
        labels = '__all__'
        widgets = {        
            'PR_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PR_CCORREO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PR_NCONTACTO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
           
        }
class formCLIENTEEXTERNO(forms.ModelForm):
    class Meta:
        model = CLIENTE_EXTERNO     
        # CLE_CDESCRIPCION
        # CLE_CCORREO
        # CLE_NCONTACTO
        # CLE_NHABILITADO
        # US_NID
        # CT_NID
	
        fields = [
        'CLE_CDESCRIPCION',
        'CLE_CCORREO',
        'CLE_NCONTACTO',
        'US_NID'

        ]
        labels = '__all__'
        widgets = {        
            'CLE_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CLE_CCORREO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CLE_NCONTACTO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
           
        }
class formCLIENTEINTERNO(forms.ModelForm):
    class Meta:
        model = CLIENTE_INTERNO     
        # CLI_CDESCRIPCION
        # CLI_CCORREO
        # CLI_NCONTACTO
        # CLI_NHABILITADO
        # US_NID
        # CT_NID
	
        fields = [
        'CLI_CDESCRIPCION',
        'CLI_CCORREO',
        'CLI_NCONTACTO',
        'US_NID'

        ]
        labels = '__all__'
        widgets = {        
            'CLI_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CLI_CCORREO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CLI_NCONTACTO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
           
        }
class formCONSULTOR(forms.ModelForm):
    class Meta:
        model = CONSULTOR     
        # CON_CDESCRIPCION
        # CON_CCORREO
        # CON_NCONTACTO
        # CON_NHABILITADO
        # US_NID
        # CT_NID
	
        fields = [
        'CON_CDESCRIPCION',
        'CON_CCORREO',
        'CON_NCONTACTO',
        'US_NID'

        ]
        labels = '__all__'
        widgets = {        
            'CON_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CON_CCORREO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CON_NCONTACTO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
           
        }
class formTRANSPORTISTA(forms.ModelForm):
    class Meta:
        model = TRANSPORTISTA     	
        fields = [
        'TR_CDESCRIPCION',
        'TR_CCORREO',
        'TR_NCONTACTO',
        'US_NID'

        ]
        labels = '__all__'
        widgets = {        
            'TR_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'TR_CCORREO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'TR_NCONTACTO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
           
        }
class formPRODUCTO(forms.ModelForm):
    class Meta:
        model = PRODUCTO     
        # TR_CDESCRIPCION
        # TR_CCORREO
        # TR_NCONTACTO
        # TR_NHABILITADO
        # US_NID
        # CT_NID
	
        fields = [
        'PC_CCODIGO_PROD',
        'PC_CDESCRIPCION',
        'PC_NCALIDAD',
        'PC_CORIGEN',
        'PC_FOTO',
        'CP_NID',
        'PC_NPESO',
        'PC_CUNIDAD_PESO',
        'PC_NREFRIGERACION',
        'PC_NPRECIO_REF',
        'PC_FFECHA_VENCIMIENTO'
        
        

        ]
        labels = '__all__'
        widgets = {        
            'PC_CCODIGO_PROD': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PC_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PC_NPRECIO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'PC_NPESO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'PC_CUNIDAD_PESO' : forms.Select(choices=[('KG','Kilogramos'),('GR','Gramos')],attrs={'class': 'form-control','type':'text'}),
            'PC_NCALIDAD' : forms.Select(choices=[(1,'Pesima'),(2,'Mala'),(3,"Calidad"),(4,"Buena"),(5,"Excelente")],attrs={'class': 'form-control','type':'text'}),
            'PC_CORIGEN': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PC_NPRECIO_REF': forms.TextInput(attrs={'class': 'form-control','type':'number','step':'1'}),
            'CP_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'PC_FFECHA_VENCIMIENTO': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'form-control','type':'datetime-local'}),
        }

class formTRANSPORTE(forms.ModelForm):
    class Meta:
        model = TRANSPORTE     
        # TR_CDESCRIPCION
        # TR_CCORREO
        # TR_NCONTACTO
        # TR_NHABILITADO
        # US_NID
        # CT_NID
	
        fields = [
        'TR_NID',
        'TRA_CPATENTE',
        'TRA_CMARCA',
        'TRA_CMODELO',
        'TRA_NCARGA',
        'TRA_NREFRIGERACION'

        ]
        labels = '__all__'
        widgets = {    
            'TR_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'TRA_CPATENTE': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'TRA_CMARCA': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'TRA_CMODELO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'TRA_NCARGA': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'TRA_NREFRIGERACION': forms.CheckboxInput(attrs={'class': 'form-control','type':'checkbox'}),
            
        }
class formOVD(forms.ModelForm):
    class Meta:
        model = ORDEN_VENTA_DETALLE    	
        fields = [
        'PC_NID',
        'OVD_NQTY',
        'OVD_NPRECIO'
        ]
        labels = '__all__'
        widgets = {        
            'OVD_NQTY': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'OVD_NPRECIO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'PC_NID': forms.Select(attrs={'class': 'form-control','type':'number'})
           
        }
class formSUD(forms.ModelForm):
    class Meta:
        model = SUBASTA_DETALLE    	
        fields = [
        'TRA_NID',
        'TR_NID',
        'SUD_NCOBRO'
        ]
        labels = '__all__'
        widgets = {        
            'SUD_NCOBRO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'TRA_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'TR_NID': forms.Select(attrs={'class': 'form-control','type':'number'})      
        }
class formOV(forms.ModelForm):
    class Meta:
        model = ORDEN_VENTA  	
        fields = [
        
        'OV_NDOCUMENTO_ORIGEN',
        'OV_CTIPO_PROCESO',
        'OV_CESTADO',
        'TC_NID',
        'US_NID',
        'OV_COBSERVACIONES'

        ]
        labels = '__all__'
        widgets = {        
            'OV_NDOCUMENTO_ORIGEN': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'OV_CTIPO_PROCESO':  forms.Select(choices=[('EXTERNO','EXTERNO'),('INTERNO','INTERNO')],attrs={'class': 'form-control','type':'text'}), 
            'OV_CESTADO':  forms.Select(choices=[('INICIADO','INICIADO'),('SELECCION','SELECCION'),('PAGO','PAGO'),('SUBASTA','SUBASTA'),('ENTREGA','ENTREGA'),('COMPLETADO','COMPLETADO'),('RECHAZADO','RECHAZADO')],attrs={'class': 'form-control','type':'text'}),
            'TC_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'OV_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control','type':'text','placeholder':'escriba sus observaciones'}),
           
        }



class formDIRECCION(forms.ModelForm):
    class Meta:
        model = DIRECCION     
        # DR_NID
        # US_NID
        # DR_CNOMBRE
        # DR_CCALLE
        # DR_CNUMERO
        # DR_CTELEFONO1
        # DR_CTELEFONO2
        # DR_NHABILITADO
	
        fields = [
        'US_NID',
        'DR_CNOMBRE',
        'DR_CCALLE',
        'DR_CNUMERO',
        'DR_CTELEFONO1',
        'DR_CTELEFONO2'


        ]
        labels = '__all__'
        widgets = {        
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'DR_CNOMBRE': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'DR_CCALLE': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'DR_CNUMERO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'DR_CTELEFONO1': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'DR_CTELEFONO2': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            

           
        }
