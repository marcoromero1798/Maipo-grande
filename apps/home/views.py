# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email import message
from modulefinder import IMPORT_NAME
from pickle import TRUE
from pydoc import cli
from webbrowser import get
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import BadHeaderError, HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render, resolve_url)
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View, TemplateView)
from apps.home.forms import *
from django.contrib import messages
from apps.home.models import CATEGARIAPRODUCTO, CONTRATO, USERS_EXTENSION, PRODUCTO
from .models import * 
import datetime as date
from .filters import ListingFilter

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

#CONTRATO
class contrato_create(CreateView):
    model = CONTRATO      # Modelo a utilizar
    form_class = formCONTRATO  # Formulario definido en forms.py
    template_name = 'home/sy-ct_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-ct_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.CT_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONTRATO',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-ct_list')
class contrato_update(UpdateView):
    model = CONTRATO      # Modelo a utilizar
    form_class = formCONTRATO  # Formulario definido en forms.py
    template_name = 'home/sy-ct_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-ct_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONTRATO',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-ct_list')
def contrato_list(request):
    try:
        context={}
        user=[]
        contrato=[]
        productor = []
        #request.user.id = USUARIO CONECTADO
        #user = queryset -> lista con sub listas
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == False:
            messages.info(request,'Usuario no habilitado, contactese con un administrador')
            return render(request,'home/sy-ct_list.html',context)
        else:
            if user.UX_IS_ADMINISTRADOR == True or user.UX_IS_CONSULTOR== True:
                contrato = CONTRATO.objects.all()
            elif user.UX_IS_PRODUCTOR == True:
                try:
                    productor = PRODUCTOR.objects.get(US_NID_id = request.user.id)
                    contrato = CONTRATO.objects.filter(PR_NID_id = productor.PR_NID)
                except Exception as e:
                    print("error al obtener datos del productor",e)
                
            else:
                messages.warning(request,'El usuario no tiene permiso para acceder, contactese con un administrador')
                return render(request,'home/sy-ct_list.html',context)
        context ={
            'object_list':contrato
        }
        return render(request,'home/sy-ct_list.html',context)

    except Exception as e:
        print("Error listar contrato: ",e)
        return render(request,'home/sy-ct_list.html',context)
def contrato_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = CONTRATO.objects.filter(CT_NID = pk).update(CT_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-ct_list")  
    messages.success(request,"Contrato Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONTRATO',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-ct_list")  

#CATEGORIA
class categoria_create(CreateView):
    model = CATEGARIAPRODUCTO      # Modelo a utilizar
    form_class = formCATEGORIA  # Formulario definido en forms.py
    template_name = 'home/sy-cp_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-cp_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.CP_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CATEGORIA',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-cp_list')
class categoria_update(UpdateView):
    model = CATEGARIAPRODUCTO      # Modelo a utilizar
    form_class = formCATEGORIA  # Formulario definido en forms.py
    template_name = 'home/sy-cp_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-cp_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CATEGORIA',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-cp_list')
def categoria_list(request):
    try:
        context={}
        user=[]
        producto=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-cp_list.html',context)
        else:
            producto = CATEGARIAPRODUCTO.objects.all()
        context ={
            'object_list':producto
        }
        return render(request,'home/sy-cp_list.html',context)

    except Exception as e:
        print("Error listar categoria: ",e)
        return render(request,'home/sy-cp_list.html',context)
def categoria_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = CATEGARIAPRODUCTO.objects.filter(CP_NID = pk).update(CP_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-cp_list")  
    messages.success(request,"Categoria Deshabilitada correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONTRATO',
                LG_CACCION ='MODIFICACION'
                )   
    historial_acciones.save() 
    return redirect("sy-cp_list")
#PRODUCTOR
class productor_create(CreateView):
    model = PRODUCTOR        # Modelo a utilizar
    form_class = formPRODUCTOR  # Formulario definido en forms.py
    template_name = 'home/sy-pr_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-pr_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.PR_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno    
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='PRODUCTOR',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-pr_list')
class productor_update(UpdateView):
    model = PRODUCTOR      # Modelo a utilizar
    form_class = formPRODUCTOR  # Formulario definido en forms.py
    template_name = 'home/sy-pr_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-pr_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='PRODUCCION',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-pr_list')
def productor_list(request):
    try:
        context={}
        user=[]
        producto=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-pr_list.html',context)
        else:
            producto = PRODUCTOR.objects.all()
        context ={
            'object_list':producto
        }
        return render(request,'home/sy-pr_list.html',context)

    except Exception as e:
        print("Error listar categoria: ",e)
        return render(request,'home/sy-pr_list.html',context)


def productor_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = PRODUCTOR.objects.filter(PR_NID = pk).update(PR_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-pr_list")  
    messages.success(request,"PRODUCTOR Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='PRODUCTOR',
                LG_CACCION ='MODIFICACION'
                )   
    historial_acciones.save() 
    return redirect("sy-pr_list")
#PRODUCTO
class producto_create(CreateView):
    model = PRODUCTO      # Modelo a utilizar
    form_class = formPRODUCTO  # Formulario definido en forms.py
    template_name = 'home/sy-pc_create.html'  # html template en core
    success_url = reverse_lazy("sy-pc_list")
    
    def form_valid(self, form, **kwargs):
        user = USERS_EXTENSION.objects.get(US_NID = self.request.user.id)
        productor = []
        if user.UX_IS_PRODUCTOR == True:
            print(self.request.user.id)
            productor = PRODUCTOR.objects.get(US_NID_id = self.request.user.id)
            form.instance.PR_NID_id = productor.PR_NID
        elif user.UX_IS_ADMINISTRADOR == True and user.UX_IS_PRODUCTOR == False:
            form.instance.PC_NID_id = self.request.user.id
        form.instance.PC_NHABILITADO = True
        retorno = super(producto_create, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='PRODUCTO',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-pc_list')
class producto_update(UpdateView):
    model = PRODUCTO      # Modelo a utilizar
    form_class = formPRODUCTO  # Formulario definido en forms.py
    template_name = 'home/sy-pc_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-pc_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='PRODUCTO',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-pc_list')
def producto_list(request):
    if request.method == "POST":
        try:
            categorias = CATEGARIAPRODUCTO.objects.all()
            context={}
            producto = PRODUCTO.objects.filter(CP_NID=request.POST.get('category'))             
            context ={
                'object_list':producto,
                'categorias':categorias, 
            }
            return render(request,'home/sy-pc_list.html',context)

        except Exception as e:
            print("Error listar productos: ",e)
            return render(request,'home/sy-pc_list.html',context)
    else:
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        categorias = CATEGARIAPRODUCTO.objects.all()
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-pc_list.html',context)
        else:
            producto = PRODUCTO.objects.all()
        context ={
                'object_list':producto, 
                'categorias':categorias,
            }
        return render(request,'home/sy-pc_list.html',context)


def producto_listone(request,pk):
    try:
        context={}
        user=[]
        producto=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-pc_listone.html',context)
        else:
            producto = PRODUCTO.objects.filter(PC_NID = pk)
        context ={
            'object_list':producto
        }
        return render(request,'home/sy-pc_listone.html',context)

    except Exception as e:
        print("Error listar productos: ",e)
        return render(request,'home/sy-pc_listone.html',context)

def producto_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = PRODUCTO.objects.filter(PC_NID = pk).update(PC_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-pc_list")  
    messages.success(request,"Producto Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='PRODUCTO',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-pc_list")  
#CLIENTE EXTERNO 
class clienteexterno_create(CreateView):
    model = CLIENTE_EXTERNO     # Modelo a utilizar
    form_class = formCLIENTEEXTERNO # Formulario definido en forms.py
    template_name = 'home/sy-cle_create.html'  # html template en core
    success_url = reverse_lazy("sy-cle_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL
        form.instance.CLE_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CLIENTE EXTERNO',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-cle_list')
class clienteexterno_update(UpdateView):
    model = CLIENTE_EXTERNO      # Modelo a utilizar
    form_class = formCLIENTEEXTERNO  # Formulario definido en forms.py
    template_name = 'home/sy-cle_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-cle_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CLIENTE EXTERNO',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-cle_list')
def clienteexterno_list(request):
    try:
        context={}
        user=[]
        clienteexterno=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-cle_list.html',context)
        else:
            clienteexterno = CLIENTE_EXTERNO.objects.all()
        context ={
            'object_list':clienteexterno
        }
        return render(request,'home/sy-cle_list.html',context)

    except Exception as e:
        print("Error listar cliente externo: ",e)
        return render(request,'home/sy-cle_list.html',context)
def clienteexterno_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = CLIENTE_EXTERNO.objects.filter(CLE_NID = pk).update(CLE_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-cle_list")  
    messages.success(request,"CLIENTE EXTERNO Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CLIENTE EXTERNO',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-cle_list")  
#CLIENTE INTERNO
class clienteinterno_create(CreateView):
    model = CLIENTE_INTERNO      # Modelo a utilizar
    form_class = formCLIENTEINTERNO  # Formulario definido en forms.py
    template_name = 'home/sy-cli_create.html'  # html template en core
    success_url = reverse_lazy("sy-cli_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.CLI_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)

        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CLIENTE INTERNO',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-cli_list')
class clienteinterno_update(UpdateView):
    model = CLIENTE_INTERNO      # Modelo a utilizar
    form_class = formCLIENTEINTERNO  # Formulario definido en forms.py
    template_name = 'home/sy-cli_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-cli_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CLIENTE INTERNO',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-cli_list')
def clienteinterno_list(request):
    try:
        context={}
        user=[]
        clienteinterno=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-ct_list.html',context)
        else:
            clienteinterno = CLIENTE_INTERNO.objects.all()
        context ={
            'object_list':clienteinterno
        }
        return render(request,'home/sy-cli_list.html',context)

    except Exception as e:
        print("Error listar cliente interno: ",e)
        return render(request,'home/sy-cli_list.html',context)
def clienteinterno_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = CLIENTE_INTERNO.objects.filter(CLI_NID = pk).update(CLI_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-cli_list")  
    messages.success(request,"CLIENTE EXTERNO Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CLIENTE INTERNO',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-cli_list")  
#CONSULTOR
class consultor_create(CreateView):
    model = CONSULTOR      # Modelo a utilizar
    form_class = formCONSULTOR  # Formulario definido en forms.py
    template_name = 'home/sy-con_create.html'  # html template en core
    success_url = reverse_lazy("sy-con_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.CON_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONSULTOR',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-con_list')
class consultor_update(UpdateView):
    model = CONSULTOR      # Modelo a utilizar
    form_class = formCONSULTOR  # Formulario definido en forms.py
    template_name = 'home/sy-con_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-con_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONSULTOR',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-con_list')
def consultor_list(request):
    try:
        context={}
        user=[]
        consultor=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-con_list.html',context)
        else:
            consultor = CONSULTOR.objects.all()
        context ={
            'object_list':consultor
        }
        return render(request,'home/sy-con_list.html',context)

    except Exception as e:
        print("Error listar consultor: ",e)
        return render(request,'home/sy-con_list.html',context)
def consultor_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = CONSULTOR.objects.filter(CON_NID = pk).update(CON_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-con_list")  
    messages.success(request,"CONSULTOR Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='CONSULTOR',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-con_list") 
#TRANSPORTISTA
class transportista_create(CreateView):
    model = TRANSPORTISTA      # Modelo a utilizar
    form_class = formTRANSPORTISTA  # Formulario definido en forms.py
    template_name = 'home/sy-tr_create.html'  # html template en core
    success_url = reverse_lazy("sy-tr_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.TR_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno    
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='TRANSPORTISTA',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-tr_list')
class transportista_update(UpdateView):
    model = TRANSPORTISTA      # Modelo a utilizar
    form_class = formTRANSPORTISTA  # Formulario definido en forms.py
    template_name = 'home/sy-tr_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-tr_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='TRANSPORTISTA',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-tr_list')
def transportista_list(request):
    try:
        context={}
        user=[]
        transportista=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-tr_list.html',context)
        else:
            transportista = TRANSPORTISTA.objects.all()
        context ={
            'object_list':transportista
        }
        return render(request,'home/sy-tr_list.html',context)

    except Exception as e:
        print("Error listar transportista: ",e)
        return render(request,'home/sy-tr_list.html',context)
def transportista_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = TRANSPORTISTA.objects.filter(TR_NID = pk).update(TR_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-tr_list")  
    messages.success(request,"TRANSPORTISTA Deshabilitado correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='TRANSPORTISTA',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-tr_list") 


def añadir_carro(request):
    context = super(CreateView, self).get_context_data(**kwargs)
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
            US_NID_id = self.request.user.id,
            LG_FFECHA_ACCION = date.datetime.now(), 
            LG_CSECCION = 'SISTEMA' ,
            LG_CMODULO='CARRO_COMPRA',
            LG_CACCION ='CREACION'
            )   
    historial_acciones.save() 
    return reverse_lazy('sy-pc_list')

def carrito_compra(request):
    cantidad = request.POST.get('cantidad')
    cantidad = request.POST.get('pc_nid')
    cantidad = request.POST.get('precio')
    
    return HttpResponse("correcto")



def info_perfil(request):
    context={}
    user=[]
    perfil=[]
    user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
    if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render (request, 'home/user-profile.html', context)
    else:
        perfil = USERS_EXTENSION.objects.filter(US_NID = request.user.id)
        context ={
         'object_list':perfil,
    }
    return render (request, 'home/user-profile.html', context)


#DIRECCION
class direccion_create(CreateView):
    model = DIRECCION      # Modelo a utilizar
    form_class = formDIRECCION  # Formulario definido en forms.py
    template_name = 'home/sy-dir_create.html'  # html template en core
    success_url = reverse_lazy("sy-dir_list") 
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        form.instance.DR_NHABILITADO = True
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='DIRECCION',
                LG_CACCION ='CREACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-dir_list')


class direccion_update(UpdateView):
    model = DIRECCION      # Modelo a utilizar
    form_class = formDIRECCION  # Formulario definido en forms.py
    template_name = 'home/sy-dir_create.html'  # html template en core
    success_url = reverse_lazy("home/sy-dir_list") 
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []        
        historial_acciones = LOG_ACCIONES(
                US_NID_id = self.request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='DIRECCION',
                LG_CACCION ='MODIFICACION'
                )   
        historial_acciones.save() 
        return reverse_lazy('sy-dir_list')


def direccion_list(request):
    try:
        context={}
        user=[]
        direccion=[]
        user = USERS_EXTENSION.objects.get(US_NID = request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(request,'Usuario no habiltado, contactese con un administrador')
            return render(request,'home/sy-dir_list.html',context)
        else:
            direccion = DIRECCION.objects.all()
        context ={
            'object_list':direccion
        }
        return render(request,'home/sy-dir_list.html',context)

    except Exception as e:
        print("Error listar direccion: ",e)
        return render(request,'home/sy-dir_list.html',context)


def direccion_deshabilitar(request,pk):
    instancia = []
    try:
        instancia = DIRECCION.objects.filter(DR_NID = pk).update(DR_NHABILITADO = False)
    except  Exception as e:
        print("error al deshabilitar :",e)
        messages.warning(request,"Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-dir_list")  
    messages.success(request,"DIRECCION Deshabilitada correctamente")
    historial_acciones = []        
    historial_acciones = LOG_ACCIONES(
                US_NID_id = request.user.id,
                LG_FFECHA_ACCION = date.datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='DIRECCION',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-dir_list") 






