# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.views import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    ################
    # MANTENEDORES #
    ################
    #CONTRATO
    path('sy-ct_create', login_required(views.contrato_create.as_view()), name='sy-ct_create'),
    path('sy-ct_list', login_required(views.contrato_list), name='sy-ct_list'),
    path('sy-ct_update/<int:pk>', login_required(views.contrato_update.as_view()), name='sy-ct_update'),
    path('sy-ct_deshabilitar/<int:pk>', login_required(views.contrato_deshabilitar), name='sy-ct_deshabilitar'),
    #CATEGORIA
    path('sy-cp_create', login_required(views.categoria_create.as_view()), name='sy-cp_create'),
    path('sy-cp_list', login_required(views.categoria_list), name='sy-cp_list'),
    path('sy-cp_list_compra', login_required(views.categoria_list_compra), name='sy-cp_list_compra'),
    path('sy-cp_update/<int:pk>', login_required(views.categoria_update.as_view()), name='sy-cp_update'),
    path('sy-cp_deshabilitar/<int:pk>', login_required(views.categoria_deshabilitar), name='sy-cp_deshabilitar'),
    #PRODUCTO
    path('sy-pc_create', login_required(views.producto_create.as_view()), name='sy-pc_create'),
    path('sy-pc_list', login_required(views.producto_list), name='sy-pc_list'),
    path('sy-pc_listone/<int:pk>', login_required(views.producto_listone), name='sy-pc_listone'),
    path('sy-pc_update/<int:pk>', login_required(views.producto_update.as_view()), name='sy-pc_update'),
    path('sy-pc_deshabilitar/<int:pk>', login_required(views.producto_deshabilitar), name='sy-pc_deshabilitar'),
    #PRODUCTOR
    path('sy-pr_create', login_required(views.productor_create.as_view()), name='sy-pr_create'),
    path('sy-pr_list', login_required(views.productor_list), name='sy-pr_list'),
    path('sy-pr_update/<int:pk>', login_required(views.productor_update.as_view()), name='sy-pr_update'),
    path('sy-pr_deshabilitar/<int:pk>', login_required(views.productor_deshabilitar), name='sy-pr_deshabilitar'),
    #CLIENTE EXTERNO
    path('sy-cle_create', login_required(views.clienteexterno_create.as_view()), name='sy-cle_create'),
    path('sy-cle_list', login_required(views.clienteexterno_list), name='sy-cle_list'),
    path('sy-cle_update/<int:pk>', login_required(views.clienteexterno_update.as_view()), name='sy-cle_update'),
    path('sy-cle_deshabilitar/<int:pk>', login_required(views.clienteexterno_deshabilitar), name='sy-cle_deshabilitar'),
    #CLIENTE INTERNO
    path('sy-cli_create', login_required(views.clienteinterno_create.as_view()), name='sy-cli_create'),
    path('sy-cli_list', login_required(views.clienteinterno_list), name='sy-cli_list'),
    path('sy-cli_update/<int:pk>', login_required(views.clienteinterno_update.as_view()), name='sy-cli_update'),
    path('sy-cli_deshabilitar/<int:pk>', login_required(views.clienteinterno_deshabilitar), name='sy-cli_deshabilitar'),
    #TRANSPORTISTA
    path('sy-tr_create', login_required(views.transportista_create.as_view()), name='sy-tr_create'),
    path('sy-tr_list', login_required(views.transportista_list), name='sy-tr_list'),
    path('sy-tr_update/<int:pk>', login_required(views.transportista_update.as_view()), name='sy-tr_update'),
    path('sy-tr_deshabilitar/<int:pk>', login_required(views.transportista_deshabilitar), name='sy-tr_deshabilitar'),
    #CONSULTOR
    path('sy-con_create', login_required(views.consultor_create.as_view()), name='sy-con_create'),
    path('sy-con_list', login_required(views.consultor_list), name='sy-con_list'),
    path('sy-con_update/<int:pk>', login_required(views.consultor_update.as_view()), name='sy-con_update'),
    path('sy-con_deshabilitar/<int:pk>', login_required(views.consultor_deshabilitar), name='sy-con_deshabilitar'),
    path('sy-envio_datos', login_required(views.carrito_compra), name='sy-envio_datos'),
    #LOG PROCESOS - LOG ACCIONES
    # path('sy-cp_create', login_required(views.categoria_create.as_view()), name='sy-cp_create'),
    # path('sy-cp_list', login_required(views.categoria_list), name='sy-cp_list'),
    #TRANSACCIONALES
    path('tr-list', login_required(views.Transacciones_list), name='tr-list'),
    # path('tr-carro_list', login_required(views.solicitud_compra_list), name='tr-carro_list'),
    #CARRITO COMPRA
    path('tr-carro_resumen/<int:us_nid>', login_required(views.carrito_compra_resumen), name='tr-carro_resumen'),
    path('tr-carro_detalle', login_required(views.carrito_compra_listone), name='tr-carro_detalle'),
    path('tr-carro_delete/<int:cc_nid>', login_required(views.carrito_compra_delete), name='tr-carro_delete'),


    #SOLICITUD COMPRA
    path('tr-sc_listone/<int:sc_nid>', login_required(views.solicitud_compra_listone), name='tr-sc_listone'),
    # path('tr-sc_list', login_required(views.solicitud_compra_list), name='tr-sc_listone'),

    #ORDEN DE VENTA
    path('tr-ov_listone/<int:ov_nid>', login_required(views.orden_venta_listone), name='tr-ov_listone'),
    path('tr-ov_create', login_required(views.OV_Create.as_view()), name='tr-ov_create'),
    path('tr-ov_update/<int:pk>', login_required(views.OV_Update.as_view()), name='tr-ov_update'),
    #ORDEN DE VENTA DETALLE
    path('tr-ovd_create/<int:ov_nid>', login_required(views.orden_venta_detalle_create), name='tr-ovd_create'),
    path('tr-ovd_update/<int:pk>', login_required(views.OVD_Update.as_view()), name='tr-ovd_update'),
    path('tr-ovd_delete/<int:id>', login_required(views.orden_venta_detalle_delete), name='tr-ovd_delete'),
    #TRASPASO
    path('tr-carro_solicitud/<int:us_nid>', login_required(views.generar_solicitud), name='tr-carro_solicitud'),
    path('tr-solicitud_orden_venta/<int:sc_nid>', login_required(views.generar_orden_venta), name='tr-solicitud_orden_venta'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
