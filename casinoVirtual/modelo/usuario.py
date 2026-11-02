# O importar una función, clase o variable específica
from werkzeug.security import generate_password_hash, check_password_hash
from db import obtener_conexion



"""
trae una consulta simple sobre informacion del usuario, buscando por correo
"""
def obtener_correo_usuario(correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT idUsuario,rol, correo, password_hash FROM usuario WHERE correo = %s",(correo,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
    
    
"""
Verifica si el usuario es correcto con sus datos y contraseñas, devuelve la info de una tabla del usuario seleccionado del correo
"""

def verificar_login(correo,contraseña):
    
    usuario = obtener_correo_usuario(correo)
    if usuario is None:
        return None
    if check_password_hash(usuario["password_hash"],contraseña):
        
        return usuario
    return None



