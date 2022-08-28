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
        'CT_FFECHA_TERMINO'
        ]
        labels = '__all__'
        widgets = {        
            'CT_FFECHA_INICIO': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'form-control','type':'datetime-local'}),
            'CT_FFECHA_TERMINO' : forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'form-control','type':'datetime-local'}),
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
        'CT_NID'

        ]
        labels = '__all__'
        widgets = {        
            'PR_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PR_CCORREO': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PR_NCONTACTO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'US_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'CT_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
           
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
        'PC_NPRECIO',
        'PC_NCALIDAD',
        'PC_CORIGEN',
        'CP_NID',
        'PR_NID',
        'PC_NPESO',
        'PC_CUNIDAD_PESO'
        

        ]
        labels = '__all__'
        widgets = {        
            'PC_CCODIGO_PROD': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PC_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'PC_NPRECIO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'PC_NPESO': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'PC_CUNIDAD_PESO': forms.Select(choices=listarOpciones("UNIDAD_MEDIDA","PM_CCODIGO","PM_CDESCRIPCION"),attrs={'class': 'js-example-responsive form-control',}),
            'PC_NCALIDAD': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'PC_CORIGEN': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
            'CP_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),
            'PR_NID': forms.Select(attrs={'class': 'form-control','type':'number'}),

           
        }
