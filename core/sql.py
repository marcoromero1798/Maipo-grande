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
        cursor.execute(
            f'SELECT "{retValue}","{retDisplay}" FROM "PARAMETRO" WHERE "PM_CGRUPO" = {sqlStr(grupo)}')

        resultado = cursor.fetchall()

        if resultado == None:
            return None
        return resultado