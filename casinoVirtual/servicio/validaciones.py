from datetime import date,datetime
import calendar
import re

def es_mayor_edad(fecha_nacimiento):
    try:
        nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    except ValueError:
        return False
    actual = date.today()
    edad = actual.year - nacimiento.year - ((actual.month, actual.day) < (nacimiento.month, nacimiento.day))
    return edad >= 18 

def convertir_vencimiento(texto):
    """Convierte 'MM/AA' en el último día de ese mes. Devuelve None si no es válido."""
    try:
        mes_txt, anio_txt = texto.split("/")
        if len(mes_txt) != 2 or len(anio_txt) != 2:
            return None
        mes = int(mes_txt)
        anio = 2000 + int(anio_txt)
    except ValueError:
        return None
    if not 1 <= mes <= 12:
        return None
    ultimo_dia = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, ultimo_dia)

def tarjeta_vigente(fecha_vencimiento):
    return fecha_vencimiento is not None and fecha_vencimiento >= date.today()

def numero_tarjeta_valido(numero):
    return re.fullmatch(r"\d{16}", numero) is not None