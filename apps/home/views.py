# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from decimal import *
import smtplib
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import BadHeaderError, HttpResponse, JsonResponse
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
from datetime import date, datetime, timedelta, timezone
import pandas as pd
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("TEST-3941599614411264-110822-6557afb20b7a8e41f42eb08f4c7f8989-340820109")
#API
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import PostSerializers
# from rest_framework import status

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

# CONTRATO
def dashboard(request):
    #FECHA CON FORMATO MESA??O
    fecha = datetime.now().strftime("%m%Y")
    ####listas#####
    #query 9
    lista_labels_query_9 = []
    lista_qty_query_9  = []
    #QUERYS
    
    #################################
    # VENTAS POR PRODUCTO - EXTERNO #
    #################################
    query_1 = ranking_productos_segun_vendidos_externo()
    #################################
    # VENTAS POR PRODUCTO - EXTERNO #
    #################################
    query_2 = ranking_productos_segun_vendidos_interno()
    ###########################
    # VENTAS TOTALES POR DIA  #
    ###########################
    query_3 = venta_por_productos_por_fecha()
    ####################################################
    # GRAFICO COMPARATIVO VENTAS EXTERNAS VS INTERNAS  #
    ####################################################
    query_4 = comparacion_venta_externa_interna()
    ###########################
    # PRODUCTO MAS VENDIDO    #
    ###########################
    query_5 = producto_mas_vendido(fecha)
    ###########################
    # CATEGORIA MAS VENDIDA   #
    ###########################
    query_6 = categoria_mas_vendida(fecha)
    ############################
    # PRODUCTOR CON MAS VENTAS #
    ############################
    query_7 = productor_con_mas_ventas(fecha)
    ##################################
    # CANTIDAD DE VENTAS COMPLETADAS #
    #################################
    query_8 = cantidad_ventas_completadas(fecha)
    ###############################
    # COMPARACION ESTADO ORDENES  #
    ###############################
    query_9 = comparacion_estado_ordenes(fecha)
    
    #############################################
    #####      REPROCESO DE CONSULTAS     #######
    #############################################
    # query 9
    for dato in query_9:
        lista_labels_query_9.append(dato[0])
        lista_qty_query_9.append(int(dato[1]))
    print(lista_labels_query_9)
    context={
        'query_1':query_1,
        'query_2':query_2,
        'query_3':query_3,
        'query_4':query_4,
        'query_5':query_5,
        'query_6':query_6,
        'query_7':query_7,
        'query_8':query_8,
        #######################
        # listas reprocesadas #
        #######################
        #query 9
        'lista_labels_query_9': lista_labels_query_9,
        'lista_qty_query_9': lista_qty_query_9
    }
    return render(request,'home/index.html',context)

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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONTRATO',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONTRATO',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-ct_list')


def contrato_list(request):
    try:
        context = {}
        user = []
        contrato = []
        productor = []
        # request.user.id = USUARIO CONECTADO
        # user = queryset -> lista con sub listas
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == False:
            messages.info(
                request, 'Usuario no habilitado, contactese con un administrador')
            return render(request, 'home/sy-ct_list.html', context)
        else:
            if user.UX_IS_ADMINISTRADOR == True or user.UX_IS_CONSULTOR == True:
                contrato = CONTRATO.objects.all()
            elif user.UX_IS_PRODUCTOR == True:
                try:
                    productor = PRODUCTOR.objects.get(
                        US_NID_id=request.user.id)
                    contrato = CONTRATO.objects.filter(
                        PR_NID_id=productor.PR_NID)
                except Exception as e:
                    print("error al obtener datos del productor", e)

            else:
                messages.warning(
                    request, 'El usuario no tiene permiso para acceder, contactese con un administrador')
                return render(request, 'home/sy-ct_list.html', context)
        context = {
            'object_list': contrato
        }
        return render(request, 'home/sy-ct_list.html', context)

    except Exception as e:
        print("Error listar contrato: ", e)
        return render(request, 'home/sy-ct_list.html', context)


def contrato_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = CONTRATO.objects.filter(
            CT_NID=pk).update(CT_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-ct_list")
    messages.success(request, "Contrato Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONTRATO',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-ct_list")

# CATEGORIA


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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CATEGORIA',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CATEGORIA',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-cp_list')


def categoria_list(request):
    try:
        context = {}
        user = []
        producto = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-cp_list.html', context)
        else:
            producto = CATEGARIAPRODUCTO.objects.all()
        context = {
            'object_list': producto
        }
        return render(request, 'home/sy-cp_list.html', context)

    except Exception as e:
        print("Error listar categoria: ", e)
        return render(request, 'home/sy-cp_list.html', context)
def stock_list(request):
    try:
        context = {}
        user = []
        producto = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-stk_list.html', context)
        else:
            stock_externa = stock_list_sql_externa()
            stock_interna = stock_list_sql_interna()
        context = {
            'object_list_interna': stock_interna,
            'object_list_externa': stock_externa
        }
        return render(request, 'home/sy-stk_list.html', context)

    except Exception as e:
        print("Error listar categoria: ", e)
        return render(request, 'home/sy-stk_list.html', context)

class stock_create(CreateView):
    model = STOCK      # Modelo a utilizar
    form_class = formSTOCK  # Formulario definido en forms.py
    template_name = 'home/sy-stk_create.html'  # html template en core
    success_url = reverse_lazy("sy-stk_list")

    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL
        form.instance.STK_CBODEGA = 'EXTERNA'
        retorno = super(CreateView, self).form_valid(form)
        return retorno

    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(CreateView, self).get_context_data(**kwargs)
        messages.success(self.request,"Stock agregado correctamente")
        return reverse_lazy('sy-stk_list')

class stock_update(UpdateView):
    model = STOCK      # Modelo a utilizar
    form_class = formSTOCK  # Formulario definido en forms.py
    template_name = 'home/sy-stk_create.html'  # html template en core
    success_url = reverse_lazy("sy-stk_list")
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL
        form.instance.STK_CBODEGA = 'EXTERNA'
        retorno = super(UpdateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        messages.success(self.request,"Stock modificado correctamente")
        return reverse_lazy('sy-stk_list')






def categoria_list_compra(request):
    try:
        context = {}
        user = []
        producto = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-cp_list_compra.html', context)
        else:
            producto = CATEGARIAPRODUCTO.objects.all()
        context = {
            'object_list': producto
        }
        return render(request, 'home/sy-cp_list_compra.html', context)
    except Exception as e:
        print("Error listar categoria: ", e)
        return render(request, 'home/sy-cp_list_compra.html', context)
def producto_list_compra(request):
    try:
        context = {}
        user = []
        producto = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-pc_list_compra.html', context)
        else:
            producto = STOCK.objects.filter(STK_CBODEGA = 'INTERNA',STK_NQTY__gt = 0)
        context = {
            'object_list': producto
        }
        return render(request, 'home/sy-pc_list_compra.html', context)
    except Exception as e:
        print("Error listar producto: ", e)
        return render(request, 'home/sy-pc_list_compra.html', context)
def categoria_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = CATEGARIAPRODUCTO.objects.filter(
            CP_NID=pk).update(CP_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-cp_list")
    messages.success(request, "Categoria Deshabilitada correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONTRATO',
                LG_CACCION='MODIFICACION'
                )
    historial_acciones.save()
    return redirect("sy-cp_list")
# PRODUCTOR


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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='PRODUCTOR',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='PRODUCCION',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-pr_list')


def productor_list(request):
    try:
        context = {}
        user = []
        producto = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-pr_list.html', context)
        else:
            producto = PRODUCTOR.objects.all()
        context = {
            'object_list': producto
        }
        return render(request, 'home/sy-pr_list.html', context)

    except Exception as e:
        print("Error listar categoria: ", e)
        return render(request, 'home/sy-pr_list.html', context)


def productor_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = PRODUCTOR.objects.filter(
            PR_NID=pk).update(PR_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-pr_list")
    messages.success(request, "PRODUCTOR Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='PRODUCTOR',
                LG_CACCION='MODIFICACION'
                )
    historial_acciones.save()
    return redirect("sy-pr_list")
# PRODUCTO


class producto_create(CreateView):
    model = PRODUCTO      # Modelo a utilizar
    form_class = formPRODUCTO  # Formulario definido en forms.py
    template_name = 'home/sy-pc_create.html'  # html template en core
    success_url = reverse_lazy("sy-pc_list")
    def form_valid(self, form, **kwargs):
        user = USERS_EXTENSION.objects.get(US_NID=self.request.user.id)
        productor = []
        if user.UX_IS_PRODUCTOR == True:
            print(self.request.user.id)
            productor = PRODUCTOR.objects.get(US_NID_id=self.request.user.id)
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='PRODUCTO',
                LG_CACCION='CREACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-pc_list')
class transporte_create(CreateView):
    model = TRANSPORTE      # Modelo a utilizar
    form_class = formTRANSPORTE # Formulario definido en forms.py
    template_name = 'home/sy-tra_create.html'  # html template en core
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = USERS_EXTENSION.objects.get(US_NID_id = self.request.user.id)
            if user.UX_IS_TRANSPORTISTA == True:
                try:
                    id_transportista = TRANSPORTISTA.objects.get(US_NID_id = self.request.user.id )
                    context['form'].fields['TR_NID'].initial = id_transportista
                    context['form'].fields['TR_NID'].disabled = True
                except Exception as e:
                    print(f"error al obtener id de transportista para usuario {self.request.user.id}: ",e)
            
        except:
            print("Error al asignar campo inicial y deshabilitado ,",e)
        
        return context
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL}
        try:
            id_tr = TRANSPORTISTA.objects.get(US_NID_id = self.request.user.id).TR_NID
        except Exception as e:
            print("error al obtener id de transportista CREATE",e)
            messages.warning(self.request,'Error al obtener el numero de transportista')
            return redirect('sy-tra_list')
        form.instance.TRA_NHABILITADO = True
        form.instance.TR_NID_id = id_tr
        retorno = super(CreateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        try:
            user = USERS_EXTENSION.objects.get(US_NID_id = self.request.user.id)
            if user.UX_IS_TRANSPORTISTA == True:
                try:
                    id_transportista = TRANSPORTISTA.objects.get(US_NID_id = self.request.user.id )
                except Exception as e:
                    print(f"error al obtener id de transportista para usuario {self.request.user.id}: ",e)
            
        except:
            print("Error al asignar campo inicial y deshabilitado ,",e)
        context = super(CreateView, self).get_context_data(**kwargs)
        historial_acciones = []
        historial_acciones = LOG_ACCIONES(
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='TRANSPORTE',
                LG_CACCION='CREACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-tra_list')
class transporte_update(UpdateView):
    model = TRANSPORTE      # Modelo a utijeclizar
    form_class = formTRANSPORTE # Formulario definido en forms.py
    template_name = 'home/sy-tra_create.html'  # html template en core
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = USERS_EXTENSION.objects.get(US_NID_id = self.request.user.id)
            if user.UX_IS_TRANSPORTISTA == True:
                try:
                    id_transportista = TRANSPORTISTA.objects.get(US_NID_id = self.request.user.id )
                    context['form'].fields['TR_NID'].initial = id_transportista
                    context['form'].fields['TR_NID'].disabled = True
                except Exception as e:
                    print(f"error al obtener id de transportista para usuario {self.request.user.id}: ",e)
            
        except:
            print("Error al asignar campo inicial y deshabilitado ,",e)
        
        return context
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL}
        try:
            id_tr = TRANSPORTISTA.objects.get(US_NID_id = self.request.user.id).TR_NID
        except Exception as e:
            print("error al obtener id de transportista ",e)
            messages.warning(self.request,'Error al obtener el numero de transportista')
            return redirect('sy-tra_list')
        form.instance.TRA_NHABILITADO = True
        form.instance.TR_NID_id = id_tr
        retorno = super(UpdateView, self).form_valid(form)
        return retorno
    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        historial_acciones = []
        historial_acciones = LOG_ACCIONES(
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='TRANSPORTE',
                LG_CACCION='ACTUALIZACION'
                )
        historial_acciones.save()
        messages.success(self.request,'Transporte modificado correctamente')
        return reverse_lazy('sy-tra_list')

def transporte_list(request):
    user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
    if user.UX_NHABILITADO == 0:
        messages.info(
            request, 'Usuario no habiltado, contactese con un administrador')
        return render(request, 'home/sy-tra_list.html', context)
    else:
        if user.UX_IS_TRANSPORTISTA == True:
            try:
                transportista = TRANSPORTISTA.objects.get(US_NID = user.US_NID_id)
                transporte = TRANSPORTE.objects.filter(TR_NID_id = transportista.TR_NID)
            except Exception as e:
                print("usuario no asociado a un id de transportista",e)
        elif user.UX_IS_ADMINISTRADOR:
            transporte = TRANSPORTE.objects.all()
    context = {
            'object_list': transporte
        }
    return render(request, 'home/sy-tra_list.html', context)

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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='PRODUCTO',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-pc_list')


def producto_list(request):
    if request.method == "POST":
        try:
            categorias = CATEGARIAPRODUCTO.objects.all()
            context = {}
            producto = PRODUCTO.objects.filter(
                CP_NID=request.POST.get('category'))
            context = {
                'object_list': producto,
                'categorias': categorias,
            }
            return render(request, 'home/sy-pc_list.html', context)

        except Exception as e:
            print("Error listar productos: ", e)
            return render(request, 'home/sy-pc_list.html', context)
    else:
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        categorias = CATEGARIAPRODUCTO.objects.all()
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-pc_list.html', context)
        else:
            producto = PRODUCTO.objects.all()
        context = {
                'object_list': producto,
                'categorias': categorias,
            }
        return render(request, 'home/sy-pc_list.html', context)


def producto_listone(request, pk):
    try:
        context = {}
        user = []
        producto = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-pc_listone.html', context)
        else:
            producto = PRODUCTO.objects.filter(PC_NID=pk)
            stock = STOCK.objects.filter(PC_NID_id = pk)
        context = {
            'object_list': producto,
            'STOCK':stock
        }
        return render(request, 'home/sy-pc_listone.html', context)

    except Exception as e:
        print("Error listar productos: ", e)
        return render(request, 'home/sy-pc_listone.html', context)


def producto_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = PRODUCTO.objects.filter(
            PC_NID=pk).update(PC_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-pc_list")
    messages.success(request, "Producto Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='PRODUCTO',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-pc_list")
# CLIENTE EXTERNO


class clienteexterno_create(CreateView):
    model = CLIENTE_EXTERNO     # Modelo a utilizar
    form_class = formCLIENTEEXTERNO  # Formulario definido en forms.py
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CLIENTE EXTERNO',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CLIENTE EXTERNO',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-cle_list')


def clienteexterno_list(request):
    try:
        context = {}
        user = []
        clienteexterno = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-cle_list.html', context)
        else:
            clienteexterno = CLIENTE_EXTERNO.objects.all()
        context = {
            'object_list': clienteexterno
        }
        return render(request, 'home/sy-cle_list.html', context)

    except Exception as e:
        print("Error listar cliente externo: ", e)
        return render(request, 'home/sy-cle_list.html', context)


def clienteexterno_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = CLIENTE_EXTERNO.objects.filter(
            CLE_NID=pk).update(CLE_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-cle_list")
    messages.success(request, "CLIENTE EXTERNO Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CLIENTE EXTERNO',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-cle_list")
# CLIENTE INTERNO


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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CLIENTE INTERNO',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CLIENTE INTERNO',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-cli_list')


def clienteinterno_list(request):
    try:
        context = {}
        user = []
        clienteinterno = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-ct_list.html', context)
        else:
            clienteinterno = CLIENTE_INTERNO.objects.all()
        context = {
            'object_list': clienteinterno
        }
        return render(request, 'home/sy-cli_list.html', context)

    except Exception as e:
        print("Error listar cliente interno: ", e)
        return render(request, 'home/sy-cli_list.html', context)


def clienteinterno_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = CLIENTE_INTERNO.objects.filter(
            CLI_NID=pk).update(CLI_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-cli_list")
    messages.success(request, "CLIENTE EXTERNO Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CLIENTE INTERNO',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-cli_list")
# CONSULTOR


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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONSULTOR',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONSULTOR',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-con_list')


def consultor_list(request):
    try:
        context = {}
        user = []
        consultor = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-con_list.html', context)
        else:
            consultor = CONSULTOR.objects.all()
        context = {
            'object_list': consultor
        }
        return render(request, 'home/sy-con_list.html', context)

    except Exception as e:
        print("Error listar consultor: ", e)
        return render(request, 'home/sy-con_list.html', context)


def consultor_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = CONSULTOR.objects.filter(
            CON_NID=pk).update(CON_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-con_list")
    messages.success(request, "CONSULTOR Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='CONSULTOR',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-con_list")
# TRANSPORTISTA


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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='TRANSPORTISTA',
                LG_CACCION='CREACION'
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
                US_NID_id=self.request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='TRANSPORTISTA',
                LG_CACCION='MODIFICACION'
                )
        historial_acciones.save()
        return reverse_lazy('sy-tr_list')

def transportista_list(request):
    try:
        context = {}
        user = []
        transportista = []
        user = USERS_EXTENSION.objects.get(US_NID=request.user.id)
        if user.UX_NHABILITADO == 0:
            messages.info(
                request, 'Usuario no habiltado, contactese con un administrador')
            return render(request, 'home/sy-tr_list.html', context)
        else:
            transportista = TRANSPORTISTA.objects.all()
        context = {
            'object_list': transportista
        }
        return render(request, 'home/sy-tr_list.html', context)

    except Exception as e:
        print("Error listar transportista: ", e)
        return render(request, 'home/sy-tr_list.html', context)

def transportista_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = TRANSPORTISTA.objects.filter(
            TR_NID=pk).update(TR_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-tr_list")
    messages.success(request, "TRANSPORTISTA Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='TRANSPORTISTA',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-tr_list")

def transporte_deshabilitar(request, pk):
    instancia = []
    try:
        instancia = TRANSPORTE.objects.filter(id=pk).update(TRA_NHABILITADO=False)
    except Exception as e:
        print("error al deshabilitar :", e)
        messages.warning(
            request, "Hubo un error al deshabilitar,contactese con un administrador")
        return redirect("sy-tra_list")
    messages.success(request, "TRANSPORTE Deshabilitado correctamente")
    historial_acciones = []
    historial_acciones = LOG_ACCIONES(
                US_NID_id=request.user.id,
                LG_FFECHA_ACCION=datetime.now(),
                LG_CSECCION='SISTEMA',
                LG_CMODULO='TRANSPORTE',
                LG_CACCION='DESHABILITADO'
                )
    historial_acciones.save()
    return redirect("sy-tra_list")


# transaccionales
# CARRO DE COMPRA
def carrito_compra(request):
    estado = True
    cantidad = request.POST.get('cantidad', 0)
    cp_nid = request.POST.get('id')
    pc_nid = request.POST.get('pc_id')
    # precio = instancia_producto.PC_NPRECIO
    # monto_total = float(precio) * int(cantidad)
    try:
        carrito_compra = []
        carrito_compra = CARRO_COMPRA(
                    US_NID_id=request.user.id,
                    PC_NID_id=pc_nid,
                    CP_NID_id=cp_nid,
                    # CC_NMONTO_TOTAL=monto_total,
                    # CC_NPRECIO=precio,
                    CC_NQTY=cantidad,
                    CC_NESTADO=True
                    )
        carrito_compra.save()
    except Exception as e:
        print("error al guardar datos en el carro de compra: ", e)
        estado = False
    return JsonResponse({
        'estado': estado
    })

def carrito_compra_listone(request):
    instancia_usuario= detalle_carro(request.user.id)
    instancia_carro = CARRO_COMPRA.objects.filter(
        US_NID_id=request.user.id, CC_NESTADO=True)
    if instancia_carro.count()== 0:
        messages.info(request,"ingrese productos al carro de compra")
    context = {
        'object_list': instancia_carro,
        'object_list_user': instancia_usuario
    }
    return render(request, 'home/tr-carro_listone.html', context)

def carrito_compra_delete(request,cc_nid):
    instancia_usuario= detalle_carro(request.user.id)
    instancia_eliminado = CARRO_COMPRA.objects.filter(CC_NID=cc_nid)
    instancia_carro = CARRO_COMPRA.objects.filter(US_NID_id=request.user.id, CC_NESTADO=True)
    context = {
        'object_list': instancia_carro,
        'object_list_user': instancia_usuario
    }
    try:
        instancia_eliminado.delete()
        messages.success(request,"Elemento eliminado correctamente")
        return render(request, 'home/tr-carro_listone.html', context)
    except Exception as e:
        messages.warning(request,"Error al eliminar el elemento, contactese con una administrador")
        print("error ",e)
        return render(request, 'home/tr-carro_listone.html', context)

def carrito_compra_resumen(request,us_nid):
    lista_elementos = []
    lista_elementos = resumen_carro(us_nid)

    return JsonResponse({
        'elementos_carro': lista_elementos
    })
# SOLICITUD DE COMPRA

def solicitud_compra_listone(request, sc_nid):
    instancia_solicitudes = SOLICITUD_COMPRA.objects.filter(SC_NID=sc_nid)
    instancia_detalle = SOLICITUD_COMPRA_DETALLE.objects.filter(SC_NID_id=sc_nid)
    # instancia_usuario = []
    # if data_clicle(request.user.id, 'cli') != None:
    #     instancia_usuario == data_clicle(request.user.id, 'cli')
    # else:
    #     instancia_usuario == data_clicle(request.user.id, 'cle')
    context = {
        'object_list': instancia_solicitudes,
        # 'object_list_usuario':instancia_usuario,
        'object_lines': instancia_detalle
    }
    return render(request, 'home/tr-sc_listone.html', context)
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


# ORDEN DE VENTA
def Transacciones_list(request):
    instancia_usuario = USERS_EXTENSION.objects.get(US_NID_id = request.user.id)
    instancia_su= []
    if instancia_usuario.UX_IS_ADMINISTRADOR == True:
        instancia_ov = ORDEN_VENTA.objects.all()
        instancia_sc = SOLICITUD_COMPRA.objects.all()
        instancia_su = SUBASTA.objects.all()
    else:
        instancia_ov = ORDEN_VENTA.objects.filter(US_NID_id = request.user.id)
        instancia_sc = SOLICITUD_COMPRA.objects.filter(US_NID_id = request.user.id)
        if instancia_usuario.UX_IS_TRANSPORTISTA == True:
            instancia_su = SUBASTA.objects.filter(US_NID_id = request.user.id)

    context = {
        'object_list_ov': instancia_ov,
        'object_list_sc': instancia_sc,
        'object_list_su': instancia_su
    }
    return render(request, 'home/tr-list.html', context)



def orden_venta_listone(request, ov_nid):
    instancia_ov = ORDEN_VENTA.objects.filter(OV_NID=ov_nid)
    SC_NID = ORDEN_VENTA.objects.get(OV_NID=ov_nid).OV_NDOCUMENTO_ORIGEN
    instancia_ovd = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id=ov_nid)
    total_iva = 0
    sub_total = 0
    for elemento in instancia_ovd:
        total_iva =total_iva + (int(elemento.OVD_NQTY) * float(elemento.OVD_NPRECIO)) * 1.19
        sub_total =sub_total + (int(elemento.OVD_NQTY) * float(elemento.OVD_NPRECIO))
    instancia_sc = SOLICITUD_COMPRA_DETALLE.objects.filter(SC_NID_id=SC_NID)
    iva = sub_total*0.19

    context = {
        'instancia_ov': instancia_ov,
        'instancia_ovd': instancia_ovd,
        'instancia_sc':instancia_sc,
        'total_iva':total_iva,
        'sub_total':sub_total,
        'iva':iva
    }
    return render(request, 'home/tr-ov_listone.html', context)


#SUBASTA 
def subasta_listone(request, su_nid):
    total_iva = 0
    OV_NID = SUBASTA.objects.get(SU_NID=su_nid).SU_NDOCUMENTO_ORIGEN_id
    #subasta
    instancia_su = SUBASTA.objects.filter(SU_NID=su_nid)
    instancia_sud = SUBASTA_DETALLE.objects.filter(SU_NID_id=su_nid)
    #transporte
    #orden venta
    instancia_ov = ORDEN_VENTA.objects.filter(OV_NID = OV_NID)
    instancia_ovd = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id = OV_NID)
    #totales
    for elemento in instancia_ovd:
        total_iva =total_iva + (int(elemento.OVD_NQTY) * float(elemento.OVD_NPRECIO)) * 1.19

    context = {
        'instancia_ov': instancia_ov,
        'instancia_ovd': instancia_ovd,
        'instancia_su':instancia_su,
        'instancia_sud':instancia_sud,
        'total_iva':total_iva,
    }
    return render(request, 'home/tr-su_listone.html', context)
def subasta_detalle_create(request, su_nid):
    form = formSUD(request.POST or None)
    if form.is_valid():
        linea = form.save(commit=False)
        #asignamos llave de la cabecera
        linea.SU_NID_id = su_nid
        #calculamos el monto total
        linea.save()
        messages.success(request,'Producto agregado correctamente')
        return redirect('tr-su_listone', su_nid)
    ctx = {
        'form': form,
        'su': su_nid,
    }
    return render(request, 'home/tr-su_create.html', ctx)

class SUD_Update(UpdateView):
    model = SUBASTA_DETALLE
    form_class = formSUD
    template_name ='home/tr-sud_create.html'
    
#    success_url = reverse_lazy('do-nv_listartodo')
    # VALIDACI??N DEL FORMULARIO ANTES DE CONTINUAR
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        context = super(UpdateView, self).get_context_data(**kwargs)

        retorno = super(SUD_Update, self).form_valid(form)
        return retorno

    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        return reverse_lazy('tr-su_listone', kwargs={'su_nid': context['object'].SU_NID_id})

def subasta_detalle_delete(request,id):
    su_nid = SUBASTA_DETALLE.objects.get(id = id).SU_NID_id
    instancia_detalle = SUBASTA_DETALLE.objects.filter(id = id)
    try:
        instancia_detalle.delete()
        messages.success(request,"Transporte eliminado correctamente")
        return redirect('tr-su_listone', su_nid)
    except Exception as e:
        print("error al eliminar ",e)
        messages.warning(request,"Error al eliminar el transporte seleccionado")
        return redirect('tr-su_listone', su_nid)
def orden_venta_detalle_create(request, ov_nid):
    form = formOVD(request.POST or None)
    if form.is_valid():

        linea = form.save(commit=False)
        #asignamos llave de la cabecera
        linea.OV_NID_id = ov_nid

        # asignar el numero de l??nea siguiente
        linea.OVD_NLINEA = nextLine_OV(ov_nid)
        #calculamos el monto total
        linea.OVD_NMONTO = linea.OVD_NPRECIO * linea.OVD_NQTY
        linea.save()

        messages.success(request,'Producto agregado correctamente')
        return redirect('tr-ov_listone', ov_nid)
    ctx = {
        'form': form,
        'ov': ov_nid,

    }
    return render(request, 'home/tr-ovd_create.html', ctx)

def orden_venta_detalle_delete(request,id):
    ov_nid = ORDEN_VENTA_DETALLE.objects.get(id = id).OV_NID
    instancia_detalle = ORDEN_VENTA_DETALLE.objects.filter(id = id)
    try:
        instancia_detalle.delete()
        messages.success(request,"Producto eliminado correctamente")
        return redirect('tr-ov_listone', ov_nid)
    except Exception as e:
        print("error al eliminar ",e)
        messages.warning(request,"Error al eliminar el producto seleccionado")
        return redirect('tr-ov_listone', ov_nid)

class OVD_Update(UpdateView):
    model = ORDEN_VENTA_DETALLE
    form_class = formOVD
    template_name ='home/tr-ovd_create.html'
    
#    success_url = reverse_lazy('do-nv_listartodo')
    # VALIDACI??N DEL FORMULARIO ANTES DE CONTINUAR
    def form_valid(self, form, **kwargs):
        # INDICA EL USUARIO ACTUAL

        context = super(UpdateView, self).get_context_data(**kwargs)

        retorno = super(OVD_Update, self).form_valid(form)
        return retorno

    def get_success_url(self, **kwargs):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        context = super(UpdateView, self).get_context_data(**kwargs)
        return reverse_lazy('tr-ov_listone', kwargs={'ov_nid': context['object'].OV_NID_id})

class OV_Create( CreateView):
    model = ORDEN_VENTA  # Modelo a utilizar
    form_class = formOV
    template_name = 'home/tr-ov_create.html'  # html template en core
    success_url = reverse_lazy("tr-list")

class OV_Update(UpdateView):
    model = ORDEN_VENTA  # Modelo a utilizar
    form_class = formOV
    template_name = 'home/tr-ov_create.html'  # html template en core
    success_url = reverse_lazy("tr-list")

# class SC_Create( CreateView):
#     model = SOLICITUD_COMPRA  # Modelo a utilizar
#     form_class = formOV
#     template_name = 'home/tr-ov_create.html'  # html template en core
#     success_url = reverse_lazy("tr-list")



#PROCESOS
# CARRO ---> SOLICITUD
def generar_solicitud(request,us_nid):
    try:
        #definicion de variables
        estado = True

        #definicion de instancias
        instancia_queryset_carro_compra = []
        instancia_queryset_solicitud_compra = []
        #obtencion de datos de la bd
        instancia_queryset_carro_compra = CARRO_COMPRA.objects.filter(US_NID_id =us_nid,CC_NESTADO = True)
        #pk que se usara en el detalle
        if instancia_queryset_carro_compra.count() > 0:

            SC_NID = nextSC_NID()
            #creamos la cabecera de solicitud de compra
            try:
                Nueva_cabecera = SOLICITUD_COMPRA(
                    SC_NID = SC_NID,
                    US_NID_id= request.user.id,
                    #DR_NID = ?
                    #TC_NID = ?
                    SC_FFECHA_CREACION = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    SC_NPROCESADO = False,
                    SC_CTIPO_SOLICITUD = 'EXTERNO'
                )
                Nueva_cabecera.save()
            except Exception as e:
                print("error al generar la cabecera de solicitud:",e)
                estado == False
            #obtenemos la nueva cabecera para ingresarla en el detalle

            linea = nextLine_SC(SC_NID)
            #almacenamos las variables
            lista_datos = []
            try:
                for elemento in instancia_queryset_carro_compra:
                    lista_aux=[]
                    Detalle = SOLICITUD_COMPRA_DETALLE(
                        SC_NID_id = SC_NID,
                        PC_NID_id = elemento.PC_NID_id,
                        CP_NID_id = elemento.CP_NID_id,
                        SC_NLINEA = linea,
                        SCD_NQTY = elemento.CC_NQTY
                    )
                    lista_datos.append(Detalle)
                    linea +=1
                SOLICITUD_COMPRA_DETALLE.objects.bulk_create(lista_datos)
            except Exception as e:
                print("Error al generar detalle de solicitud: ",e)
                estado = False
            if estado == True:
                instancia_queryset_carro_compra.update(CC_NESTADO = False)
        else:
            messages.info(request,'Ingrese elementos al carro de compra')
            return redirect('tr-carro_detalle')
    except Exception as e:
        print("error traspaso de carro a solicitud de compra: ",e)
        messages.warning(request,'Error al traspasar el carro de compra a solicitud de compra, contactese con un administrador')
        return redirect('tr-carro_detalle')
    messages.success(request,f"Solicitud creada correctamente, Nro solicitud:{SC_NID}")
    return  redirect('tr-list')
# SOLICITUD ---> OV
def generar_orden_venta(request,sc_nid):
    try:
        #definicion de variables
        estado = True

        #definicion de instancias
        instancia_queryset_solicitud_compra = []
        #obtencion de datos de la bd
        instancia_queryset_solicitud_compra = SOLICITUD_COMPRA.objects.filter(SC_NID =sc_nid)
        instancia_queryset_solicitud_detalle = SOLICITUD_COMPRA_DETALLE.objects.filter(SC_NID_id =sc_nid)
        #pk que se usara en el detalle


        OV_NID = nextOV_NID()
        #creamos la cabecera de solicitud de compra
        try:
            Nueva_cabecera = ORDEN_VENTA(
                OV_NID = OV_NID,
                OV_NDOCUMENTO_ORIGEN_id = sc_nid,
                OV_CESTADO = 'INICIADO',
                OV_CTIPO_PROCESO = 'EXTERNO',
                OV_NPROCESADO = False,
                OV_FFECHA_CREACION = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                US_NID_id= request.user.id,
                #DR_NID = ?
                #TC_NID = ?
                OV_FFECHA_PROCESAMIENTO= None,
                OV_COBSERVACIONES = ''
            )
            Nueva_cabecera.save()
        except Exception as e:
            print("error al generar la cabecera de solicitud:",e)
            estado == False
        #obtenemos la nueva cabecera para ingresarla en el detalle
        if estado == True:
            instancia_queryset_solicitud_compra.update(SC_NPROCESADO = True,SC_FFECHA_PROCESAMIENTO = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            messages.info(request,'Ingrese elementos al carro de compra')
            return reverse_lazy('tr-carro_detalle',kwargs = {'sc_nid':sc_nid})
    except Exception as e:
        print("error traspaso de carro a solicitud de compra: ",e)
        messages.warning(request,'Error al traspasar la solicitud de compra a orden de venta, contactese con un administrador')
        return reverse_lazy('tr-carro_detalle',kwargs = {'sc_nid':sc_nid})
    messages.success(request,f"Orden de venta creada correctamente, Nro Orden de venta :{OV_NID}")
    return  redirect('tr-list')
# PROCESO EXTERNO   
def generar_orden_venta_completa(request,sc_nid):
    try:
        #definicion de variables
        estado = True

        #definicion de instancias
        instancia_queryset_solicitud_compra = []
        #obtencion de datos de la bd
        instancia_queryset_solicitud_compra = SOLICITUD_COMPRA.objects.filter(SC_NID =sc_nid)
        instancia_queryset_solicitud_detalle = SOLICITUD_COMPRA_DETALLE.objects.filter(SC_NID_id =sc_nid)
        #pk que se usara en el detalle
        OV_NID = nextOV_NID()
        #creamos la cabecera de solicitud de compra
        try:
            Nueva_cabecera = ORDEN_VENTA(
                OV_NID = OV_NID,
                OV_NDOCUMENTO_ORIGEN_id = sc_nid,
                OV_CESTADO = 'INICIADO',
                OV_CTIPO_PROCESO = 'INTERNO',
                OV_NPROCESADO = False,
                OV_FFECHA_CREACION = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                US_NID_id= request.user.id,
                #DR_NID = ?
                #TC_NID = ?
                OV_FFECHA_PROCESAMIENTO= None,
                OV_COBSERVACIONES = ''
            )
            Nueva_cabecera.save()
        except Exception as e:
            print("error al generar la cabecera de ov:",e)
            estado == False
        linea = nextLine_OV(OV_NID)
        try:
            lista_datos = []
            try:
                for elemento in instancia_queryset_solicitud_detalle:
                    precio_prod = elemento.PC_NID.PC_NPRECIO_REF
                    lista_aux=[]
                    Detalle = ORDEN_VENTA_DETALLE(
                        OV_NID_id = OV_NID,
                        PC_NID_id = elemento.PC_NID_id,
                        CP_NID_id = elemento.CP_NID_id,
                        OVD_NLINEA = linea,
                        OVD_NQTY = elemento.SCD_NQTY,
                        OVD_NPRECIO = precio_prod
                    )
                    lista_datos.append(Detalle)
                    linea +=1
                ORDEN_VENTA_DETALLE.objects.bulk_create(lista_datos)
            except Exception as e:
                print("Error al generar detalle de OV: ",e)
                estado = False

        except Exception as e:
            print("error al generar el detalle de solicitud:",e)
            estado == False
        #obtenemos la nueva cabecera para ingresarla en el detalle
        if estado == True:
            instancia_queryset_solicitud_compra.update(SC_NPROCESADO = True,SC_FFECHA_PROCESAMIENTO = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return redirect('tr-list')
    except Exception as e:
        print("error traspaso de solicitud de compra a orden de venta: ",e)
        messages.warning(request,'Error al traspasar la solicitud de compra a orden de venta, contactese con un administrador')
        return redirect('tr-list')
    messages.success(request,f"Orden de venta creada correctamente, Nro Orden de venta :{OV_NID}")
    return  redirect('tr-list')
# OV ---> SUBASTA:
def generar_subasta(request,ov_nid):
    estado = True
    #elementos importante de la subasta
    req_refrigeracion = False
    peso_total = 0
    
    #definicion de instancias
    instancia_queryset_orden_venta = []
    #obtencion de datos de la bd
    instancia_queryset_orden_venta = ORDEN_VENTA.objects.get(OV_NID = ov_nid)
    instancia_queryset_orden_venta_detalle = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id =ov_nid)
    peso_acum = 0
    #pk que se usara en el detalle
    for elemento in instancia_queryset_orden_venta_detalle:
        id_producto = elemento.PC_NID_id

        try:
            instancia_producto = PRODUCTO.objects.get(PC_NID = id_producto)
        except Exception as e:
            print("error al obtener datos del producto:",e)
            estado = False

        #??requiere refrigeracion?
        if instancia_producto.PC_NREFRIGERACION == True:
            req_refrigeracion = True
        if instancia_producto.PC_CUNIDAD_PESO == 'GR':
            peso_acum = peso_acum + (instancia_producto.PC_NPESO/1000) 
        else:
            peso_acum = peso_acum + instancia_producto.PC_NPESO 

    peso_total = peso_acum
    
    SU_NID = nextSU_NID()
    try:
        Nueva_cabecera = SUBASTA(
            SU_NID = SU_NID,
            SU_NDOCUMENTO_ORIGEN_id = ov_nid,
            SU_NREFRIGERACION = req_refrigeracion,
            SU_PESO_TOTAL = peso_total,
            DR_NID = instancia_queryset_orden_venta.DR_NID_id,
            US_NID_id= instancia_queryset_orden_venta.US_NID_id
        )
        Nueva_cabecera.save()
        
    except Exception as e:
        print("error al generar la cabecera de subasta",e)
        estado = False
    #actualizacion estado OV
    if estado == True:
        ORDEN_VENTA.objects.filter(OV_NID = ov_nid).update(
                OV_CESTADO = 'SUBASTA',
                OV_NPROCESADO = True,
                OV_FFECHA_PROCESAMIENTO = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
        messages.success(request,'Subasta generada correctamente')
        return redirect('tr-list')
    else:
        messages.warning(request,'Ocurrio un error al generar una nueva subasta')
        return redirect('tr-list')
     
#INICIAR SUBASTA
def iniciar_subasta(request,su_nid):
   
    context={
        'fecha_actual':datetime.now().strftime('%Y-%m-%d')
    }
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio',None)
        fecha_termino = request.POST.get('fecha_termino',None)
        if fecha_inicio == None :
            messages.warning(request,'Ingrese una fecha valida')
            return render(request,'home/tr-su_iniciar.html',context)
        elif fecha_termino == None:
            messages.warning(request,'Ingrese una fecha valida')
            return render(request,'home/tr-su_iniciar.html',context)
        else:
            try:
                fecha_inicio_format = datetime.fromisoformat(fecha_inicio).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                fecha_termino_format = datetime.fromisoformat(fecha_termino).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                SUBASTA.objects.filter(SU_NID = su_nid).update(SU_FFECHA_INICIO = fecha_inicio_format, SU_FFECHA_TERMINO = fecha_termino_format,SU_NPROCESADO = True)
                messages.success(request,'Proceso de subasta iniciado correctamente')
                return redirect('tr-su_listone',su_nid)
            except Exception as e:
                print("error al modificar la fechas de subasta: ", e)
                messages.warning(request,'Error al modificar la fechas de subasta')
                return render(request,'home/tr-su_iniciar.html',context)
    else:
        return render(request,'home/tr-su_iniciar.html',context)
#TERMINAR SUBASTA
def terminar_subasta(request,su_nid):
    #TRANSPORTE SELECCIONADO 
    ID_TRANSPORTE_SELECCIONADO  = 0
    ID_DETALLE_SUBASTA_SELECCIONADO  = 0
    #LISTA DE TRANSPORTES OPTIMOS
    LISTA_TRANSPORTES_OPTIMOS =[]
    #BUSCAR LOS TRANSPORTES ASOCIADOS A LA SUBASTA Y LLOS DATOS DE LA SUBASTA
    transportes_subasta = SUBASTA_DETALLE.objects.filter(SU_NID_id = su_nid)
    #BUSCAMOS DATOS DE LA SUBASTA
    if transportes_subasta.count()>0:
        try:
            info_subasta = SUBASTA.objects.get(SU_NID = su_nid)
            ORDEN_VENTA_id = info_subasta.SU_NDOCUMENTO_ORIGEN_id
            requiere_refrigeracion = info_subasta.SU_NREFRIGERACION
            peso_minimo_req = info_subasta.SU_PESO_TOTAL
        except Exception as e:
            print("error al obtener datos de la subasta", e)
            return redirect('tr-su_listone',su_nid) 
        #ITERAMOS PARA ENCONTRAR EL TRANSPORTE MAS BARATO, QUITANDO LOS QUE NO CUMPLAN REQUISITOS MINIMOS DE LA SUBASTA
        for transporte in transportes_subasta:
            #lista auxiliar para igresar los datos ordenados en formato [[x,y],[x,y]]
            lista_aux = []
            #OBTENEMOS DATOS DE LOS TRANSPORTES QUE CUMPLAN LAS NORMAS
            datos_transporte = TRANSPORTE.objects.get(id = transporte.TRA_NID_id)
            #FILTRAMOS
            if requiere_refrigeracion == True:
                if datos_transporte.TRA_NREFRIGERACION == requiere_refrigeracion:
                    if datos_transporte.TRA_NCARGA >= peso_minimo_req:
                        lista_aux.append(transporte.TRA_NID)        #id transporte
                        lista_aux.append(transporte.id)             #id SU DETALLE 
                        lista_aux.append(transporte.SUD_NCOBRO)     #PRECIO
                        LISTA_TRANSPORTES_OPTIMOS.append(lista_aux)
            else:
                if datos_transporte.TRA_NCARGA >= peso_minimo_req:
                    lista_aux.append(transporte.TRA_NID)        #id transporte
                    lista_aux.append(transporte.id)             #id SU DETALLE 
                    lista_aux.append(transporte.SUD_NCOBRO)     #PRECIO
                    LISTA_TRANSPORTES_OPTIMOS.append(lista_aux)
        if len(LISTA_TRANSPORTES_OPTIMOS) >0:
            #ORDENAMOS EL DF PARA SABER CUAL ES TRANSPORTE QUE TENGA MENOR COBRO, EN EL CASO DE QUE EL COBRO SEA EL MISMO SE ELEGIRA EN BASE AL ID DE SUBASTA DETALLE
            dataframe = pd.DataFrame(LISTA_TRANSPORTES_OPTIMOS,columns=['id_transporte','id_subasta_id','precio'])
            dataframe_ordenado = dataframe.sort_values(by=['id_subasta_id', 'precio'],ascending=[True,True])
            #TRANSPORTE SELECCIONADO
            #########################################################################################
            ID_TRANSPORTE_SELECCIONADO =  dataframe_ordenado["id_transporte"].loc[0]                #
            ID_DETALLE_SUBASTA_SELECCIONADO =  dataframe_ordenado["id_subasta_id"].loc[0]           #
            #########################################################################################

            #####################################
            # modificamos los campos necesarios # 
            #####################################
            SUBASTA_DETALLE.objects.filter(id = ID_DETALLE_SUBASTA_SELECCIONADO).update(SUD_NSELECCION = True)
            SUBASTA.objects.filter(SU_NID = su_nid).update(SU_NTRANSPORTE_SELECCIONADO = ID_TRANSPORTE_SELECCIONADO,SU_NESTADO = True)
            ORDEN_VENTA.objects.filter(OV_NID = ORDEN_VENTA_id).update(OV_CESTADO = 'ENVIADO')
            #################
            # notificacion ##
            #################
            #TRANSPORTISTA 
            ov = SUBASTA.objects.get(SU_NID =su_nid).SU_NDOCUMENTO_ORIGEN
            correo = TRANSPORTISTA.objects.get(TR_NID = TRANSPORTE.objects.get(id = ID_TRANSPORTE_SELECCIONADO.id).TR_NID_id).TR_CCORREO
            send_email_notificacion_documentos(correo, mensaje_OV(request,ov))
            messages.success(request,'Subasta concluida correctamente')
            return redirect('tr-su_listone',su_nid) 
        else:
            messages.warning(request,'No hay transportes que cumplan con las condiciones de la subasta')
            return redirect('tr-su_listone',su_nid)    
    else:
        messages.warning(request,'No hay transportes participando en la subasta')
        return redirect('tr-su_listone',su_nid)      
#OBTENER MEJOR PRODUCTO
def obtener_mejor_producto(request,ov_nid):
    ##############################################
    # a considerar en este codigo
    # el flujo es el siguiente
    # SOLICITUD(ID)-->SOLICITUD DETALLE ---> CATEGORIA DE PRODUCTO ---->PRODUCTOS ASOCIADOS ----> STOCK-----> OVD
    #############################################
    #OBTENGO EL ID DE SOLICITUD
    sc_nid = request.POST.get('sc_nid',None)
    #DEFINO VARIABLES PARA PARAMETROS
    minimo_calidad = 3
    estado = True
    fecha_minima = datetime.now() +  timedelta(days=31)
    fecha_minima_formato = fecha_minima.strftime("%Y-%m-%d")
    #variables
    categoria = ''
    mensaje = ''
    qty = 0
    #listas

    lista_categorias = []
    lista_bulk = []
    cant_lineas = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id = ov_nid).count()
    if sc_nid != None:
        #OBTENGO LOS DATOS DEL DETALLE DE LA SOLICITUD GRACIAS AL ID DE LA CABECERA
        solicitudes = SOLICITUD_COMPRA_DETALLE.objects.filter(SC_NID_id = sc_nid)
        for elemento in solicitudes:
            lista_aux = []
            categoria = elemento.CP_NID
            qty = elemento.SCD_NQTY
            lista_aux.append(categoria)
            lista_aux.append(qty)
            #CREO UN UNA LISTA CON ESTE FORMATO [[CATEGORIA,CANTIDAD],[CATEGORIA,CANTIDAD]] DONDE:
            #  CATEGORIA ES LA CATEGORIA DE PRODUCTO SOLICITADA
            #  CANTIDAD ES LA CANTIDAD TOTAL SOLICITADA PARA ESA CATEGORIA
            lista_categorias.append(lista_aux)
            if cant_lineas > 1:
                linea_ovd = nextLine_OV(ov_nid)
            else:
                linea_ovd = 1
        #RECORRO LA LISTA DE CATEGORIAS ASIGNANDO DOS VARIABLES A CADA POSICION
        for categoria,cantidad in lista_categorias:
            listado_productos = []
            #DEFINO LA LINEA INICIAL, UNA OV VACIA INICIA CON LINEA 0 sino inicia con la ultima linea ingresada
            #OBTENGO LOS PRODUCTOS ASOCIADOS A LA CATEGORIA ORDENADOS POR LA CALIDAD
            productos = PRODUCTO.objects.filter(CP_NID_id = categoria.CP_NID,PC_NHABILITADO = True).order_by('-PC_NCALIDAD')
            #RECORRO LA LISTA DE PRODUCTOS ASOCIADOS A LA CATEGORIA
            for valor in productos:
                lista_aux=[]
                try:
                    stock_asociado = STOCK.objects.get(PC_NID_id = valor.PC_NID,STK_CBODEGA ='EXTERNA').STK_NQTY
                except :
                    stock_asociado = 0
                #almacenamos las variables que seran utilizadas para determinar la importancia
                pc_nid = valor.PC_NID
                precio_base = valor.PC_NPRECIO_REF
                calidad = valor.PC_NCALIDAD
                vencimiento = valor.PC_FFECHA_VENCIMIENTO
                fecha_formateada = vencimiento.strftime("%Y-%m-%d")

                # FILTRO LOS DATOS EN BASE A LA CATEGORIA, SI SU FECHA DE VENCIMIENTO ES VALIDA Y SI TIENE STOCK
                if calidad >= minimo_calidad:
                    if fecha_formateada > fecha_minima_formato:
                        if stock_asociado > 0:
                            lista_aux.append(pc_nid)            #pos 0
                            lista_aux.append(precio_base)       #pos 1
                            lista_aux.append(calidad)           #pos 1
                            lista_aux.append(stock_asociado)    #pos 2
                            listado_productos.append(lista_aux)

            #TRANSFORMO LA LISTA EN UN DATAFRAME PARA ORDENAR LA LISTA
            dataframe = pd.DataFrame(listado_productos,columns=['id','precio','calidad','stk'])
            dataframe_ordenado = dataframe.sort_values(by=['calidad', 'precio'],ascending=[False,True])

            suma_cantidad = 0
            diferencia = 0
            lista_updates = []
            stock_necesario = cantidad #cantidad es lo que se solicito de la categoria
            #REALIZO EL CALCULO AL DATAFRAME DETERMINANDO CUANTO STOCK DE CADA PRODUCTO SE LE ASIGNARA EN LA ORDEN DE VENTA
            for index,row in dataframe_ordenado.iterrows():
                nuevo_objeto = ''
                lista_aux_updates= []
                pc_nid = row[0]
                precio = row[1]
                stock = row[3]
                #SI EL STOCK DEL PRODUCTO ES MAYOR AL NECESITADO, SE CALCULA LA DIFERENCIA, SE ALMACENA LO NECESITADO, Y SE ACTUALIZA EL STOCK
                #SI EL STOCK ES 0 SE CIERRA EL CICLO
                if stock_necesario == 0:
                    break
                else:
                    if stock >= stock_necesario:
                        try:
                            #SE ALMACENA EL STOCK FINAL DEL PRODUCTO PARA ACTUALIZARLO EN LA TABLA STOCK
                            stock_final = stock - stock_necesario
                            nuevo_objeto = ORDEN_VENTA_DETALLE(
                                OV_NID_id = ov_nid,
                                PC_NID_id = pc_nid,
                                CP_NID_id = categoria.CP_NID,
                                OVD_NQTY = cantidad,
                                OVD_NPRECIO = precio,
                                OVD_NLINEA = linea_ovd
                            )
                            lista_bulk.append(nuevo_objeto)
                            lista_aux_updates.append(pc_nid)
                            lista_aux_updates.append(stock_final)
                            lista_updates.append(lista_aux_updates)
                            linea_ovd +=1
                            stock_necesario = 0
                        except Exception as e:
                            print("error al ingresar stock en ovd 1 :",e)
                            estado = False
                    elif stock < stock_necesario:
                        try:
                            stock_necesario = stock_necesario - stock
                            stock_final = 0
                            nuevo_objeto = ORDEN_VENTA_DETALLE(
                                OV_NID_id = ov_nid,
                                PC_NID_id = pc_nid,
                                CP_NID_id = categoria.CP_NID,
                                OVD_NQTY = stock,
                                OVD_NPRECIO = precio,
                                OVD_NLINEA = linea_ovd
                            )
                            lista_bulk.append(nuevo_objeto)
                            lista_aux_updates.append(pc_nid)
                            lista_aux_updates.append(stock_final)
                            lista_updates.append(lista_aux_updates)
                            linea_ovd +=1
                        except Exception as e:
                            print("error al ingresar stock en ovd 2 :",e)
                            estado = False
            #EN EL CASO DE QUE EL STOCK NECESARIO SEA MAYOR QUE 0 IMPLICA QUE NO SE ALCANZO A CUBRIR LA TOTALIDAD DE LA DEMANDA CON LOS PRODUCTOS
            #ENCONTRADOS
            #SE ACTUALIZA EL ESTADO DE CADA LINEA DE LA SOLICITUD PARA NOTIFICAR SI UN PRODUCTO ESTA PENDIENTE EN EL SISTEMA

            if stock_necesario >= 0:
                print("no se pudo cubrir la totalidad de la demanda con productos de buena calidad:",categoria.CP_CDESCRIPCION)
                
                mensaje = mensaje + f'''{categoria.CP_CDESCRIPCION} <br>'''
                SOLICITUD_COMPRA_DETALLE.objects.filter(CP_NID_id= categoria.CP_NID,SC_NID_id = sc_nid).update(SCD_NESTADO = False)
            else:
                SOLICITUD_COMPRA_DETALLE.objects.filter(CP_NID_id= categoria.CP_NID,SC_NID_id = sc_nid).update(SCD_NESTADO = True)
        #SE CREAN LOS PRODUCTOS EN EL DETALLE Y SE ACTUALIZA EL STOCK
        if estado == True:
            try:
                ORDEN_VENTA_DETALLE.objects.bulk_create(lista_bulk)
                ORDEN_VENTA.objects.filter(OV_NID = ov_nid).update(OV_CESTADO = 'SELECCION')
            except Exception as e:
                print("error al crear la OVD ",e)
            for elemento in lista_updates:
                STOCK.objects.filter(PC_NID_id= elemento[0],STK_CBODEGA= 'EXTERNA').update(STK_NQTY = elemento[1])

            return JsonResponse({
                'Estado':estado,
                'mensaje':mensaje
            })
        else:
            return JsonResponse({
                'Estado':estado,
                'mensaje':mensaje
            })
def send_email_notificacion_documentos(correo_dest, message):
    try:
        msg = MIMEMultipart()
        password = 'fwgrosbdtqoleqgf'
        msg['From'] = 'sender.neuronia@gmail.com'
        msg['To'] = correo_dest
        msg['Subject'] = f'Notificicacion de pedido'

        msg.attach(MIMEText(message, _subtype='html'))
        server = smtplib.SMTP(f'{"smtp.gmail.com"}:{587}')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

        print("mensaje enviado correctamente")
    except Exception as e:
        print(e)
def traspasar_stock(request):
    #buscamos la totalidad de  stock ingresado 
    STOCK_VENTA_EXTERNA = STOCK.objects.filter(STK_CBODEGA="EXTERNA",STK_NQTY__gt = 0)
    if STOCK_VENTA_EXTERNA.count() > 0:
        for venta_externa in STOCK_VENTA_EXTERNA:
            id_producto = venta_externa.PC_NID_id
            STOCK_VENTA_INTERNA = STOCK.objects.filter(STK_CBODEGA ="INTERNA",PC_NID =id_producto)
            if STOCK_VENTA_INTERNA.count() == 0:
                nuevo_stock = STOCK(
                    PC_NID_id = id_producto,
                    STK_NQTY = venta_externa.STK_NQTY,
                    STK_CBODEGA = 'INTERNA'
                )
                nuevo_stock.save()
                STOCK.objects.filter(PC_NID_id = id_producto,STK_CBODEGA="EXTERNA").update(STK_NQTY = 0)
            else:
                try:
                    stock_interno = STOCK.objects.get(PC_NID_id = id_producto,STK_CBODEGA="INTERNA").STK_NQTY
                    stock_externo = venta_externa.STK_NQTY
                    #calculo de stock interno mas externo para traspasar al stock interno

                    stock_final = stock_externo + stock_interno
                    #STOCK INTERNO ACTUALIZADO CON EL STOCK EXTERNO
                    STOCK.objects.filter(PC_NID_id = id_producto,STK_CBODEGA="INTERNA").update(STK_NQTY = stock_final)
                    #STOCK EXTERNO ACTUALIZADO CON EL STOCK EN 0
                    STOCK.objects.filter(PC_NID_id = id_producto,STK_CBODEGA="EXTERNA").update(STK_NQTY = 0)

                except Exception as e:
                    
                    print("error al obtener datos del stock asociados al producto: ",e)

        messages.success(request,'Stock traspasado correctamente')
        return redirect('sy-stk_list')
    else:
        messages.warning(request,'No se encontraron productos con stock EXTERNO')
        return redirect('sy-stk_list')


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
                LG_FFECHA_ACCION = datetime.now(), 
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
                LG_FFECHA_ACCION = datetime.now(), 
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
                LG_FFECHA_ACCION = datetime.now(), 
                LG_CSECCION = 'SISTEMA' ,
                LG_CMODULO='DIRECCION',
                LG_CACCION ='DESHABILITADO'
                )   
    historial_acciones.save() 
    return redirect("sy-dir_list") 





def mensaje_OV(request,ov):
    instancia_ov = ORDEN_VENTA.objects.get(OV_NID = ov.OV_NID)
    instancia_ovd = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id = ov.OV_NID)
    instancia_subasta = SUBASTA.objects.get(SU_NDOCUMENTO_ORIGEN = ov.OV_NID)
    cobro_transporte = SUBASTA_DETALLE.objects.get(SU_NID_id = instancia_subasta.SU_NID, SUD_NSELECCION= True).SUD_NCOBRO
    string_texto= ''
    total = 0
    for elemento in instancia_ovd:
        total = total + round((elemento.OVD_NPRECIO * elemento.OVD_NQTY),0)



    mensaje = '''
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
                <head>
                <!--[if gte mso 9]>
                <xml>
                <o:OfficeDocumentSettings>
                    <o:AllowPNG/>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
                </xml>
                <![endif]-->
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="x-apple-disable-message-reformatting">
                <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
                <title></title>
                
                    <style type="text/css">
                    @media only screen and (min-width: 620px) {
                .u-row {
                    width: 600px !important;
                }
                .u-row .u-col {
                    vertical-align: top;
                }

                .u-row .u-col-31p67 {
                    width: 190.02px !important;
                }

                .u-row .u-col-33p33 {
                    width: 199.98px !important;
                }

                .u-row .u-col-35 {
                    width: 210px !important;
                }

                .u-row .u-col-50 {
                    width: 300px !important;
                }

                .u-row .u-col-66p67 {
                    width: 400.02px !important;
                }

                .u-row .u-col-100 {
                    width: 600px !important;
                }

                }

                @media (max-width: 620px) {
                .u-row-container {
                    max-width: 100% !important;
                    padding-left: 0px !important;
                    padding-right: 0px !important;
                }
                .u-row .u-col {
                    min-width: 320px !important;
                    max-width: 100% !important;
                    display: block !important;
                }
                .u-row {
                    width: calc(100% - 40px) !important;
                }
                .u-col {
                    width: 100% !important;
                }
                .u-col > div {
                    margin: 0 auto;
                }
                .no-stack .u-col {
                    min-width: 0 !important;
                    display: table-cell !important;
                }

                .no-stack .u-col-31p67 {
                    width: 31.67% !important;
                }

                .no-stack .u-col-33p33 {
                    width: 33.33% !important;
                }

                .no-stack .u-col-35 {
                    width: 35% !important;
                }

                .no-stack .u-col-50 {
                    width: 50% !important;
                }

                .no-stack .u-col-66p67 {
                    width: 66.67% !important;
                }

                }
                body {
                margin: 0;
                padding: 0;
                }

                table,
                tr,
                td {
                vertical-align: top;
                border-collapse: collapse;
                }

                .ie-container table,
                .mso-container table {
                table-layout: fixed;
                }

                * {
                line-height: inherit;
                }

                a[x-apple-data-detectors='true'] {
                color: inherit !important;
                text-decoration: none !important;
                }

                table, td { color: #000000; } @media (max-width: 480px) { #u_content_image_4 .v-container-padding-padding { padding: 20px 5px 5px !important; } #u_content_image_4 .v-src-width { width: auto !important; } #u_content_image_4 .v-src-max-width { max-width: 49% !important; } #u_content_image_5 .v-container-padding-padding { padding: 20px 5px 5px !important; } #u_content_image_5 .v-src-width { width: auto !important; } #u_content_image_5 .v-src-max-width { max-width: 30% !important; } #u_content_heading_3 .v-container-padding-padding { padding: 10px 10px 39px !important; } #u_content_image_6 .v-container-padding-padding { padding: 21px 5px 5px !important; } #u_content_image_6 .v-src-width { width: auto !important; } #u_content_image_6 .v-src-max-width { max-width: 46% !important; } #u_content_heading_4 .v-container-padding-padding { padding: 14px 10px 39px !important; } #u_content_heading_5 .v-container-padding-padding { padding: 10px !important; } #u_content_heading_5 .v-font-size { font-size: 14px !important; } #u_content_heading_6 .v-container-padding-padding { padding: 10px !important; } #u_content_heading_6 .v-font-size { font-size: 14px !important; } #u_content_heading_7 .v-container-padding-padding { padding: 10px !important; } #u_content_heading_7 .v-font-size { font-size: 14px !important; } #u_content_heading_10 .v-container-padding-padding { padding: 10px !important; } #u_content_heading_11 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_12 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_22 .v-container-padding-padding { padding: 11px 10px 10px !important; } #u_content_heading_23 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_24 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_19 .v-container-padding-padding { padding: 10px !important; } #u_content_heading_20 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_21 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_17 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_18 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_14 .v-container-padding-padding { padding: 40px 10px !important; } #u_content_heading_30 .v-container-padding-padding { padding: 40px 10px 39px !important; } #u_content_heading_31 .v-container-padding-padding { padding: 33px 10px 31px 22px !important; } #u_content_heading_15 .v-container-padding-padding { padding: 20px 10px !important; } }
                    </style>
                
                

                <!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Montserrat:400,700&display=swap" rel="stylesheet" type="text/css"><!--<![endif]-->

                </head>

                <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">
                <!--[if IE]><div class="ie-container"><![endif]-->
                <!--[if mso]><div class="mso-container"><![endif]-->
                <table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0">
                <tbody>
                <tr style="vertical-align: top">
                    <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->
                    

                <div class="u-row-container" style="padding: 0px;background-image: url('https://i.postimg.cc/xTPbNXWQ/image-3.png');background-repeat: no-repeat;background-position: center top;background-color: transparent">
                <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
                    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-image: url('images/image-3.png');background-repeat: no-repeat;background-position: center top;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
                    
                <!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
                <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:30px 10px 251px 30px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <h1 class="v-font-size" style="margin: 0px; color: #1b1c4a; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 40px;">
                    <strong>Orden de venta</strong>
                </h1>

                    </td>
                    </tr>
                </tbody>
                </table>

                <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                    <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                    </div>
                </div>
                </div>



                <div class="u-row-container" style="padding: 0px;background-color: transparent">
                <div class="u-row no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
                    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
                    
                <!--[if (mso)|(IE)]><td align="center" width="199" style="background-color: #ffffff;width: 199px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 199.98px;display: table-cell;vertical-align: top;">
                <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table id="u_content_image_4" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 5px 5px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td style="padding-right: 0px;padding-left: 0px;" align="center">
                    
                    <img align="center" border="0" src="https://i.postimg.cc/bJQvXMPP/image-2.png" alt="Barcode " title="Barcode " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 27%;max-width: 51.29px;" width="51.29" class="v-src-width v-src-max-width"/>
                    
                    </td>
                </tr>
                </table>

                    </td>
                    </tr>
                </tbody>
                </table>

                <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:12px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
                '''    
    mensaje = mensaje + f'''Orden de venta NO: <strong>{ov.OV_NID}</strong> '''
    mensaje = mensaje +'''  </h1>

                    </td>
                    </tr>
                </tbody>
                </table>

                <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="210" style="background-color: #ffffff;width: 210px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-35" style="max-width: 320px;min-width: 210px;display: table-cell;vertical-align: top;">
                <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table id="u_content_image_5" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 5px 5px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td style="padding-right: 0px;padding-left: 0px;" align="center">
                    
                    <img align="center" border="0" src="https://i.postimg.cc/8kmCtqwB/image-4.png" alt="Calendar " title="Calendar " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 17%;max-width: 34px;" width="34" class="v-src-width v-src-max-width"/>
                    
                    </td>
                </tr>
                </table>

                    </td>
                    </tr>
                </tbody>
                </table>

                <table id="u_content_heading_3" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">''' 
    mensaje = mensaje + f'''Fecha: <strong>{datetime.now().strftime("%d-%m-%Y")}</strong> '''
    mensaje = mensaje + '''
            </h1>

                </td>
                </tr>
            </tbody>
            </table>

            <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
            </div>
            </div>
            <!--[if (mso)|(IE)]></td><![endif]-->
            <!--[if (mso)|(IE)]><td align="center" width="190" style="background-color: #ffffff;width: 190px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
            <div class="u-col u-col-31p67" style="max-width: 320px;min-width: 190.02px;display: table-cell;vertical-align: top;">
            <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
            <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
            
            <table id="u_content_image_6" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
            <tbody>
                <tr>
                <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:41px 5px 5px;font-family:arial,helvetica,sans-serif;" align="left">
                    
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td style="padding-right: 0px;padding-left: 0px;" align="center">
                
                <img align="center" border="0" src="https://i.postimg.cc/FRq1VmD9/image-1.png" alt="Dollar " title="Dollar " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 28%;max-width: 50.41px;" width="50.41" class="v-src-width v-src-max-width"/>
                
                </td>
            </tr>
            </table>

                </td>
                </tr>
            </tbody>
            </table>

            <table id="u_content_heading_4" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
            <tbody>
                <tr>
                <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:12px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
                    
            <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">'''
    mensaje = mensaje + f'''Total transporte: <strong>{round(cobro_transporte,0)}</strong>'''
    mensaje = mensaje + '''</h1>

                        </td>
                        </tr>
                    </tbody>
                    </table>

                    <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                    </div>
                    </div>
                    <!--[if (mso)|(IE)]></td><![endif]-->
                        <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                        </div>
                    </div>
                    </div>



                <div class="u-row-container" style="padding: 0px;background-color: transparent">
                <div class="u-row no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
                    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
                    
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                <div style="background-color: #1b1c4a;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table id="u_content_heading_5" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <h1 class="v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
                    <strong>Codigo producto</strong>
                </h1>

                    </td>
                    </tr>
                </tbody>
                </table>

                <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                <div style="background-color: #1b1c4a;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table id="u_content_heading_6" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <h1 class="v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
                    <strong>Cantidad</strong>
                </h1>

                    </td>
                    </tr>
                </tbody>
                </table>

                <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                <div style="background-color: #1b1c4a;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table id="u_content_heading_7" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
                        
                <h1 class="v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
                    <strong>Total</strong>
                </h1>

                    </td>
                    </tr>
                </tbody>
                </table>

                <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                    <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                    </div>
                </div>
                </div> '''

    for elemento in instancia_ovd:

        string_texto =  string_texto + '''<div class="u-row-container" style="padding: 0px;background-color: transparent">
                <div class="u-row no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
                    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
                    
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #ffffff;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
                <table id="u_content_heading_10" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                <tbody>
                    <tr>
                    <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 11px;font-family:arial,helvetica,sans-serif;" align="left">     
                    <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">'''
        string_texto =  string_texto + elemento.PC_NID.PC_CCODIGO_PROD
        string_texto =  string_texto + '''</h1>
                    </td>
                    </tr>
                </tbody>
                </table>

                <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #ffffff;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                
<table id="u_content_heading_11" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
        
  <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
'''
        string_texto =  string_texto +  f'''<strong>{elemento.OVD_NQTY}</strong>'''
        string_texto =  string_texto + '''  </h1>

                        </td>
                        </tr>
                    </tbody>
                    </table>

                    <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
                    </div>
                    </div>
                    <!--[if (mso)|(IE)]></td><![endif]-->
                    <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #ffffff;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                    <div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                    <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                    <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
                    
                    <table id="u_content_heading_12" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                    <tbody>
                        <tr>
                        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
                            
                    <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">'''
        string_texto =  string_texto + f'''<strong>{round((elemento.OVD_NQTY * elemento.OVD_NPRECIO),0)}</strong>'''
        string_texto =  string_texto +  '''
        </h1>

            </td>
            </tr>
        </tbody>
        </table>

        <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
        </div>
        </div>
        <!--[if (mso)|(IE)]></td><![endif]-->
            <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
            </div>
        </div>
        </div>




        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
            <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
            <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
            
        <!--[if (mso)|(IE)]><td align="center" width="400" style="background-color: #ffffff;width: 400px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
        <div class="u-col u-col-66p67" style="max-width: 320px;min-width: 400px;display: table-cell;vertical-align: top;">
        <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
        '''
    mensaje= mensaje + string_texto + '''
<table id="u_content_heading_31" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px 20px 270px;font-family:arial,helvetica,sans-serif;" align="left">
        
  <h1 class="v-font-size" style="margin: 0px; color: #1b1c4a; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 20px;">

        <strong>TOTAL</strong>
  </h1>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
  <div style="background-color: #1b1c4a;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_heading_15" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
        
  <h1 class="v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">'''
    mensaje= mensaje + f'''<strong>{total}</strong>''''''
  </h1>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>




    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
    </td>
  </tr>
  </tbody>
  </table>
  <!--[if mso]></div><![endif]-->
  <!--[if IE]></div><![endif]-->
</body>

</html>

'''
    return mensaje
def perfil(request,us_nid):

    return render(request, 'home/user-profile.html')


def distribuir_pago(request,ov_nid):
    try:
        OV_DATA = ORDEN_VENTA.objects.get(OV_NID = ov_nid)
        OV_DETALLE = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id = ov_nid)
        #PARA DISTRUIR EL PAGO PRIMERO DETERMINAMOS EN UNA LISTA CON SUB LISTAS CUAL ES EL PRODUCTOR Y CUALES SON SUS PRODUCTOS
        lista_distribucion = []
        lista_insercion = []
        #PARA ALMACENAR LOS DATOS 



        for linea_detalle in OV_DETALLE:

            ################################
            cantidad = 0
            precio = 0
            productor = 0
            detalle = []
            ################################
            precio = linea_detalle.OVD_NPRECIO
            productor = linea_detalle.PC_NID.PR_NID.US_NID_id
            cantidad = linea_detalle.OVD_NQTY
            #################################
            detalle = PAGO_CUENTA(
                US_NID_id = productor,
                PCA_FFECHA = datetime.now(),
                PCA_NQTY = cantidad,
                PCA_NPRECIO = precio,
                PCA_OV_ORIGEN_id = ov_nid
            )
            lista_insercion.append(detalle)
        PAGO_CUENTA.objects.bulk_create(lista_insercion)
        # ACTUALIZAMOS EL ESTADO DE LA ORDEN DE VENTA
        ORDEN_VENTA.objects.filter(OV_NID = ov_nid).update(OV_CESTADO = 'COMPLETADO')
        messages.success(request,"Pagos distribuidos correctamente")
        return redirect("tr-list")
    except Exception as e: 
        print("error al distribuir el pago :",e)
        messages.warning(request,"Error al distribuir el pago")
        return redirect("tr-list")
def pagar(request,ov_nid):
    data_cliente = []
    instancia_ov = ORDEN_VENTA.objects.filter(OV_NID=ov_nid)
    try:
        usuario_ov = ORDEN_VENTA.objects.get(OV_NID=ov_nid)
    except Exception as e:
        print(e)
    SC_NID = ORDEN_VENTA.objects.get(OV_NID=ov_nid).OV_NDOCUMENTO_ORIGEN
    instancia_ovd = ORDEN_VENTA_DETALLE.objects.filter(OV_NID_id=ov_nid)
    try:
        if CLIENTE_EXTERNO.objects.filter(US_NID_id = usuario_ov.US_NID).count() > 0:
            data_cliente.append(request.user.first_name)
            data_cliente.append(request.user.last_name)
            data_cliente.append(CLIENTE_EXTERNO.objects.get(US_NID_id = usuario_ov.US_NID).CLE_CCORREO)        
        else:
            data_cliente.append(request.user.first_name)
            data_cliente.append(request.user.last_name)
            data_cliente.append(CLIENTE_INTERNO.objects.get(US_NID_id = usuario_ov.US_NID).CLI_CCORREO) 
    except Exception as e :
        print("Error al obtener usuarios",e)
    total_iva = 0
    sub_total = 0
    for elemento in instancia_ovd:
        total_iva =total_iva + (int(elemento.OVD_NQTY) * float(elemento.OVD_NPRECIO)) * 1.19
        sub_total =sub_total + (int(elemento.OVD_NQTY) * float(elemento.OVD_NPRECIO))

    instancia_sc = SOLICITUD_COMPRA_DETALLE.objects.filter(SC_NID_id=SC_NID)

    instancia_su = SUBASTA.objects.get(SU_NDOCUMENTO_ORIGEN = ov_nid)
    instancia_sud = SUBASTA_DETALLE.objects.get(SU_NID_id = instancia_su.SU_NID,SUD_NSELECCION = True)

    transportista = TRANSPORTISTA.objects.get(TR_NID = instancia_sud.TR_NID_id).TR_CDESCRIPCION
    iva = sub_total*0.19
    preference_data = {
        "items" : [],
        "payer": {
            "name":'',
            "surname":'',
            "email":''
        },
        "external_reference": 0
    }
    for linea in instancia_ovd:
        producto = PRODUCTO.objects.get(PC_NID = linea.PC_NID_id)
        preference_data['items'].append(
            {
            "title": f"{producto.PC_CCODIGO_PROD} {producto.PC_CDESCRIPCION}",
            "quantity": linea.OVD_NQTY,
            "unit_price": int(linea.OVD_NPRECIO),
            }
        ) 
    #agregamos datos del camion y su cobro
    preference_data['items'].append({
            "title": f"Courier: {transportista}",
            "quantity": 1,
            "unit_price": int(instancia_sud.SUD_NCOBRO),
            })
    # Crea un ??tem en la preferencia
    # if data_cliente != None:
    #     preference_data['payer']["name"] = data_cliente[0]
    #     preference_data['payer']["surname"]= data_cliente[1]
    #     preference_data['payer']["email"]= data_cliente[2]
    try:
        url_notifaction = PARAMETRO.objects.get(PM_CGRUPO = 'URL',PM_CCODIGO = 'PAGO').PM_CVALOR1
    except Exception as e:
        print("error queryset url api pago: ",e)
    preference_data['notification_url']= url_notifaction +'/pago/'
    preference_data['external_reference']= ov_nid
    

   
    # preference_json = json.dumps(preference_data)
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]['id']
    

    context = {
        'instancia_ov': instancia_ov,
        'instancia_ovd': instancia_ovd,
        'instancia_sc':instancia_sc,
        'total_iva':total_iva,
        'sub_total':sub_total,
        'iva':iva,
        'preference':preference
    }
    return render(request, 'home/tr-ov_listone_pagar.html', context)


def marcar_como_entregado(request,ov_nid):
    try:
        ORDEN_VENTA.objects.filter(OV_NID = ov_nid).update(OV_CESTADO = 'ENTREGADO')
        messages.success(request,"Orden de venta marcada como entregada correctamente")
    except Exception as e:
        print("Error al editar orden de venta ",e)
    redirect('tr-list')