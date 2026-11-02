from datetime import date,datetime
def es_mayor_edad(fecha_nacimiento):
    try:
        nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    except ValueError:
        return False
    actual = date.today()
    edad = actual.year - nacimiento.year - ((actual.month, actual.day) < (nacimiento.month, nacimiento.day))
    return edad >= 18 
        