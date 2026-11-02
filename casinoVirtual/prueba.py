from werkzeug.security import generate_password_hash, check_password_hash
from modelo.usuario import obtener_correo_usuario,verificar_login
from servicio.registro import registrar_usuario
from servicio.validaciones import es_mayor_edad
"""Login"""
#correo = input("Ingresa el correo: ")
#contraseña = input("contraseña: ")
#print(verificar_login(correo, contraseña))
""" 
nombre = input("Ingrese nombre: ")
correo = input("Ingrese correo: ")
contraseña = input("Ingrese contraseña: ")
telefono = input("Ingrese telefono: ")
direccion = input("Ingrese direccion: ")
fecha_nacimiento = input("Ingrese fecha_nacimiento: ")

registrar_usuario(correo, contraseña, nombre, telefono, direccion, fecha_nacimiento)
"""
"""
fecha_nacimiento = input("Fecha: ")
print(es_mayor_edad(fecha_nacimiento))
"""