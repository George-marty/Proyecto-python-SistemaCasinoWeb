from werkzeug.security import generate_password_hash, check_password_hash
from modelo.usuario import obtener_correo_usuario,verificar_login

correo = input("Ingresa el correo: ")
contraseña = input("contraseña: ")
print(verificar_login(correo, contraseña))



