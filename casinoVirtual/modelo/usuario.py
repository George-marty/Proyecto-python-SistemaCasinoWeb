# O importar una función, clase o variable específica
from werkzeug.security import generate_password_hash, check_password_hash
from db import obtener_conexion



"""
trae una consulta simple sobre informacion del usuario, buscando por correo
"""
def obtener_correo_usuario(correo):
    
    cursor = obtener_conexion().cursor(dictionary=True)
    cursor.execute("SELECT idUsuario,rol, correo, password_hash FROM usuario WHERE correo = %s",(correo,))
    resultado = cursor.fetchone()
    return resultado
    
    
"""
Verifica si el usuario es correcto con sus datosy contraseñas, devuelve la info de una tabla del usuario seleccionado del correo
"""

def verificar_login(correo,contraseña):
    cursor = obtener_conexion()
    usuario = obtener_correo_usuario(correo)
    if usuario is None:
        return None
    if check_password_hash(usuario["password_hash"],contraseña):
        variable = obtener_correo_usuario()
        cursor.close()
        return usuario
    return None



