from django.db import connection

def sqlStr(text):
    try:
        text = text.replace("'", "")
        text = "'"+text+"'"
        return text
    except Exception as e:
        return text


def sqlNumber(text1):
    try:
        text = str(text1)
        indice = text.rfind('.')
        decimales = '0'
        numero = text

        if indice >= 0:
            decimales = text[indice+1:5]
        else:
            indice = text.rfind(',')
            if indice >= 0:
                decimales = text[indice+1:5]
        if indice >= 0:
            numero = text[0:indice]
        text = str(numero)+str('.')+str(decimales)
        text = text.replace("$", "")
        print(text, ' numero:', numero, ' decimales:', decimales)
        return text
    except Exception as e:
        print(e)
        return text


def formatearFecha_YYYYMMDD(text):
    try:
        dia = text[0:2]
        mes = text[3:5]
        ano = text[6:10]
        fecha = f"{ano}-{mes}-{dia}"
        return fecha
    except Exception as e:
        return text


def formatearFecha_YYYYMMDD_validar(text):
    try:
        dia = text[0:2]
        mes = text[3:5]
        ano = text[6:10]
        fecha = f"{ano}-{mes}-{dia}"
        return fecha
    except Exception as e:
        return None

def listarOpciones(grupo, retValue, retDisplay):
    resultado = listarParametros(grupo, retValue, retDisplay)
    return tuple(tuple(sub) for sub in resultado)

def listarParametros(grupo, retValue, retDisplay):
    with connection.cursor() as cursor:
        cquery = f'SELECT "{retValue}","{retDisplay}" FROM "PARAMETRO" WHERE "PM_CGRUPO" = {sqlStr(grupo)}'
        print(cquery)
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def nextLine_OV(ov_nid):
    with connection.cursor() as cursor:
        cquery = f'select COALESCE(max("OVD_NLINEA"),0) + 1 from "ORDEN_VENTA_DETALLE" where "OV_NID_id" = {ov_nid}'
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        return resultado[0]

def nextLine_SC(sc_nid):
    with connection.cursor() as cursor:
        cquery = f'select COALESCE(max("SC_NLINEA"),0) + 1 from "SOLICITUD_COMPRA_DETALLE" where "SC_NID_id" = {sc_nid}'
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        return resultado[0]

def nextSC_NID():
    with connection.cursor() as cursor:
        cquery = f'select COALESCE(max("SC_NID"),0) + 1  from "SOLICITUD_COMPRA"'
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        return resultado[0]
def nextOV_NID():
    with connection.cursor() as cursor:
        cquery = f'select COALESCE(max("OV_NID"),0) + 1  from "ORDEN_VENTA"'
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        return resultado[0]
def resumen_carro(US_NID):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT 
        "PRODUCTO"."PC_CDESCRIPCION",
        "CARRO_COMPRA"."CC_NQTY"
        FROM "CARRO_COMPRA" 
        LEFT JOIN "PRODUCTO"  ON "PRODUCTO"."PC_NID" = "CARRO_COMPRA"."PC_NID_id"
        WHERE "CARRO_COMPRA"."CC_NESTADO" = TRUE 
        AND "CARRO_COMPRA"."US_NID_id" = {US_NID}'''

        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def detalle_carro(US_NID):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT
        "USERS_EXTENSION"."UX_CRUT",
        "USERS_EXTENSION"."UX_CTELEFONO",
        CASE 
        WHEN "CLIENTE_INTERNO"."CLI_CCORREO" is NULL THEN "CLIENTE_EXTERNO"."CLE_CCORREO"
        end as correo



        FROM "USERS_EXTENSION"
        LEFT JOIN "CLIENTE_EXTERNO" ON "CLIENTE_EXTERNO"."US_NID_id" = "USERS_EXTENSION"."US_NID_id"
        LEFT JOIN "CLIENTE_INTERNO" ON "CLIENTE_INTERNO"."US_NID_id" = "USERS_EXTENSION"."US_NID_id"
        WHERE "USERS_EXTENSION"."US_NID_id" = {US_NID}'''

        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def stock_list_sql():
    with connection.cursor() as cursor:
        cquery = f'''
            SELECT 
            "PRODUCTO"."PC_NID",
            "PRODUCTO"."PC_CCODIGO_PROD",
            "PRODUCTO"."PC_CDESCRIPCION",
            "STOCK"."STK_NQTY",	
            "STOCK"."STK_NID"	

            FROM "PRODUCTO"
            LEFT JOIN "STOCK" ON "STOCK"."PC_NID_id" = "PRODUCTO"."PC_NID" 
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def data_clicle(us_nid,tabla):
    if tabla == 'cle':
        cquery = f'''
        SELECT 
        "CLE_NID", 
        "CLE_CDESCRIPCION", 
        "CLE_CCORREO", 
        "CLE_NCONTACTO", 
        "CLE_NHABILITADO",
        "US_NID_id"
        FROM auth_user
        LEFT JOIN "CLIENTE_EXTERNO" AS "CLE" ON "CLE"."US_NID_id" = auth_user.id
        WHERE auth_user.id = {us_nid}'''
    else:
        cquery = f'''
        SELECT 
        "CLI_NID", 
        "CLI_CDESCRIPCION", 
        "CLI_CCORREO", 
        "CLI_NCONTACTO", 
        "CLI_NHABILITADO",
        "US_NID_id"
        FROM auth_user
        LEFT JOIN "CLIENTE_INTERNO" AS "CLI" ON "CLI"."US_NID_id" = auth_user.id
        WHERE auth_user.id = {us_nid}'''
    with connection.cursor() as cursor:
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado