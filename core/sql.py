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
def nextSU_NID():
    with connection.cursor() as cursor:
        cquery = f'select COALESCE(max("SU_NID"),0) + 1  from "SUBASTA"'
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        return resultado[0]
def resumen_carro(US_NID):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT 
		"PRODUCTO"."PC_CDESCRIPCION",
        "CATEGORIA_PRODUCTO"."CP_CDESCRIPCION",
		"CARRO_COMPRA"."CC_NQTY"
        FROM "CARRO_COMPRA" 
        LEFT JOIN "CATEGORIA_PRODUCTO" on "CATEGORIA_PRODUCTO"."CP_NID" = "CARRO_COMPRA"."CP_NID_id"
        LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "CARRO_COMPRA"."PC_NID_id"
		WHERE "CARRO_COMPRA"."CC_NESTADO" = TRUE 
        AND "CARRO_COMPRA"."US_NID_id" =  {US_NID}'''

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
def detalle_solicitud(CP_NID,SC_NID):
    with connection.cursor() as cursor:
        cquery = f'''
                SELECT 
                    SUM(SD."SCD_NQTY") AS CANTIDAD_SC
                FROM "SOLICITUD_COMPRA_DETALLE" AS SD
                LEFT JOIN "CATEGORIA_PRODUCTO" AS CP ON CP."CP_NID" = SD."CP_NID_id"

                WHERE CP."CP_NID" IS NOT NULL AND CP."CP_NID" = {CP_NID} AND SD."SC_NID_id" = {SC_NID}
                GROUP BY CP."CP_NID",SD."SC_NID_id" '''

        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado[0]
def detalle_ov(CP_NID,SC_NID):
    with connection.cursor() as cursor:
        cquery = f'''
SELECT 

SUM(OVD."OVD_NQTY") AS CANTIDAD_OV
FROM "ORDEN_VENTA_DETALLE" AS OVD
LEFT JOIN "ORDEN_VENTA" AS OV ON OV."OV_NID" = OVD."OV_NID_id"
LEFT JOIN "PRODUCTO" AS PC ON OVD."PC_NID_id" = PC."PC_NID"
LEFT JOIN "CATEGORIA_PRODUCTO" AS CP ON CP."CP_NID" = PC."CP_NID_id"
WHERE OV."OV_NDOCUMENTO_ORIGEN_id" = {SC_NID} and CP."CP_NID" ={CP_NID}
GROUP BY CP."CP_NID",OV."OV_NDOCUMENTO_ORIGEN_id"
'''

        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado[0]
def stock_list_sql_externa():
    with connection.cursor() as cursor:
        cquery = f'''
            SELECT 
            "PRODUCTO"."PC_NID",
            "PRODUCTO"."PC_CCODIGO_PROD",
            "PRODUCTO"."PC_CDESCRIPCION",
            "STOCK"."STK_NQTY",	
            "STOCK"."STK_NID",	
            "STOCK"."STK_CBODEGA"	

            FROM "PRODUCTO"
            LEFT JOIN "STOCK" ON "STOCK"."PC_NID_id" = "PRODUCTO"."PC_NID" 
            WHERE "STOCK"."STK_CBODEGA" = 'EXTERNA'
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def stock_list_sql_interna():
    with connection.cursor() as cursor:
        cquery = f'''
            SELECT 
            "PRODUCTO"."PC_NID",
            "PRODUCTO"."PC_CCODIGO_PROD",
            "PRODUCTO"."PC_CDESCRIPCION",
            "STOCK"."STK_NQTY",	
            "STOCK"."STK_NID",	
            "STOCK"."STK_CBODEGA"	

            FROM "PRODUCTO"
            LEFT JOIN "STOCK" ON "STOCK"."PC_NID_id" = "PRODUCTO"."PC_NID"
            WHERE "STOCK"."STK_CBODEGA" = 'INTERNA' 
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
    
def ranking_productos_segun_vendidos_externo():
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT
        "PRODUCTO"."PC_CDESCRIPCION",
        SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
        FROM "ORDEN_VENTA"
        LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA"."OV_NID" = "ORDEN_VENTA_DETALLE"."OV_NID_id"
        LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
        WHERE "PC_NID_id" is NOT NULL AND "ORDEN_VENTA"."OV_CTIPO_PROCESO" ='EXTERNO'
        GROUP BY "PRODUCTO"."PC_CDESCRIPCION";
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado

def ranking_productos_segun_vendidos_interno():
    with connection.cursor() as cursor:
        cquery = f'''
    SELECT
    "PRODUCTO"."PC_CDESCRIPCION",
    SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
    FROM "ORDEN_VENTA"
    LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA"."OV_NID" = "ORDEN_VENTA_DETALLE"."OV_NID_id"
    LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
    WHERE "PC_NID_id" is NOT NULL AND "ORDEN_VENTA"."OV_CTIPO_PROCESO" ='INTERNO'
    GROUP BY "PRODUCTO"."PC_CDESCRIPCION";
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def venta_por_productos_por_fecha():
    with connection.cursor() as cursor:
        cquery = f'''
    SELECT
    to_char("ORDEN_VENTA"."OV_FFECHA_CREACION",'YYYY/MM/DD'),
    SUM("ORDEN_VENTA"."OV_NID")
    FROM "ORDEN_VENTA"
    LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA"."OV_NID" = "ORDEN_VENTA_DETALLE"."OV_NID_id"
    LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
    WHERE "PC_NID_id" is NOT NULL AND "ORDEN_VENTA"."OV_CTIPO_PROCESO" ='INTERNO'
    GROUP BY to_char("ORDEN_VENTA"."OV_FFECHA_CREACION",'YYYY/MM/DD');
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def comparacion_venta_externa_interna():
    with connection.cursor() as cursor:
        cquery = f'''
            SELECT
            "ORDEN_VENTA"."OV_CTIPO_PROCESO",
            SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
            FROM "ORDEN_VENTA"
            LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA"."OV_NID" = "ORDEN_VENTA_DETALLE"."OV_NID_id"
            LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
            WHERE "PC_NID_id" is NOT NULL AND "ORDEN_VENTA"."OV_CTIPO_PROCESO" ='EXTERNO'
            GROUP BY "ORDEN_VENTA"."OV_CTIPO_PROCESO"
            UNION ALL
            SELECT
            "ORDEN_VENTA"."OV_CTIPO_PROCESO",
            SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
            FROM "ORDEN_VENTA"
            LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA"."OV_NID" = "ORDEN_VENTA_DETALLE"."OV_NID_id"
            LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
            WHERE "PC_NID_id" is NOT NULL AND "ORDEN_VENTA"."OV_CTIPO_PROCESO" ='INTERNO'
            GROUP BY "ORDEN_VENTA"."OV_CTIPO_PROCESO";
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
def producto_mas_vendido(MESAÑO):
    with connection.cursor() as cursor:
        cquery = f'''
            SELECT "PRODUCTO"."PC_CDESCRIPCION",SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
            FROM "ORDEN_VENTA"
            LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA_DETALLE"."OV_NID_id" = "ORDEN_VENTA"."OV_NID"
            LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
            LEFT JOIN "CATEGORIA_PRODUCTO" ON "CATEGORIA_PRODUCTO"."CP_NID" = "PRODUCTO"."CP_NID_id"
            WHERE TO_CHAR("ORDEN_VENTA"."OV_FFECHA_PROCESAMIENTO",'mmyyyy') ='{MESAÑO}' 
            and "ORDEN_VENTA"."OV_CESTADO" = 'COMPLETADO'
            GROUP BY "PRODUCTO"."PC_CDESCRIPCION"
            ORDER BY SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY") DESC
            LIMIT 1
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado[0]
def categoria_mas_vendida(MESAÑO):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT "CATEGORIA_PRODUCTO"."CP_CDESCRIPCION",SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
        FROM "ORDEN_VENTA"
        LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA_DETALLE"."OV_NID_id" = "ORDEN_VENTA"."OV_NID"
        LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
        LEFT JOIN "CATEGORIA_PRODUCTO" ON "CATEGORIA_PRODUCTO"."CP_NID" = "PRODUCTO"."CP_NID_id"
        WHERE TO_CHAR("ORDEN_VENTA"."OV_FFECHA_PROCESAMIENTO",'mmyyyy') ='{MESAÑO}' 
        and "ORDEN_VENTA"."OV_CESTADO" = 'COMPLETADO'
        GROUP BY "CATEGORIA_PRODUCTO"."CP_CDESCRIPCION"
        ORDER BY SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY") DESC
        LIMIT 1
        ;
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado[0]
def productor_con_mas_ventas(MESAÑO):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT "PRODUCTOR"."PR_CDESCRIPCION",SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY")
        FROM "ORDEN_VENTA"
        LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA_DETALLE"."OV_NID_id" = "ORDEN_VENTA"."OV_NID"
        LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
        LEFT JOIN "PRODUCTOR" ON "PRODUCTOR"."PR_NID" = "PRODUCTO"."PR_NID_id"
        LEFT JOIN "CATEGORIA_PRODUCTO" ON "CATEGORIA_PRODUCTO"."CP_NID" = "PRODUCTO"."CP_NID_id"
        WHERE TO_CHAR("ORDEN_VENTA"."OV_FFECHA_PROCESAMIENTO",'mmyyyy') ='{MESAÑO}' 
        and "ORDEN_VENTA"."OV_CESTADO" = 'COMPLETADO'
        GROUP BY "PRODUCTOR"."PR_CDESCRIPCION"
        ORDER BY SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY") DESC
        LIMIT 1
        ;
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado[0]
def cantidad_ventas_completadas(MESAÑO):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT SUM("ORDEN_VENTA"."OV_NID")
        FROM "ORDEN_VENTA"
        LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA_DETALLE"."OV_NID_id" = "ORDEN_VENTA"."OV_NID"
        LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
        LEFT JOIN "PRODUCTOR" ON "PRODUCTOR"."PR_NID" = "PRODUCTO"."PR_NID_id"
        LEFT JOIN "CATEGORIA_PRODUCTO" ON "CATEGORIA_PRODUCTO"."CP_NID" = "PRODUCTO"."CP_NID_id"
        WHERE TO_CHAR("ORDEN_VENTA"."OV_FFECHA_PROCESAMIENTO",'mmyyyy') ='{MESAÑO}' 
        and "ORDEN_VENTA"."OV_CESTADO" = 'COMPLETADO'
        GROUP BY TO_CHAR("ORDEN_VENTA"."OV_FFECHA_PROCESAMIENTO",'mmyyyy')
        ORDER BY SUM("ORDEN_VENTA_DETALLE"."OVD_NQTY") DESC
        LIMIT 1
        ;
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchone()
        if resultado == None:
            return None
        return resultado[0]
def comparacion_estado_ordenes(MESAÑO):
    with connection.cursor() as cursor:
        cquery = f'''
        SELECT 
        "ORDEN_VENTA"."OV_CESTADO" as ESTADO,
        SUM("ORDEN_VENTA"."OV_NID") as SUMA
        FROM "ORDEN_VENTA"
        LEFT JOIN "ORDEN_VENTA_DETALLE" ON "ORDEN_VENTA_DETALLE"."OV_NID_id" = "ORDEN_VENTA"."OV_NID"
        LEFT JOIN "PRODUCTO" ON "PRODUCTO"."PC_NID" = "ORDEN_VENTA_DETALLE"."PC_NID_id"
        LEFT JOIN "PRODUCTOR" ON "PRODUCTOR"."PR_NID" = "PRODUCTO"."PR_NID_id"
        LEFT JOIN "CATEGORIA_PRODUCTO" ON "CATEGORIA_PRODUCTO"."CP_NID" = "PRODUCTO"."CP_NID_id"
        WHERE TO_CHAR("ORDEN_VENTA"."OV_FFECHA_PROCESAMIENTO",'mmyyyy') ='{MESAÑO}' 
        GROUP BY "ORDEN_VENTA"."OV_CESTADO"
        ;
            '''
        cursor.execute(cquery)
        resultado = cursor.fetchall()
        if resultado == None:
            return None
        return resultado
