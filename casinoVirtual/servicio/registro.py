from werkzeug.security import generate_password_hash, check_password_hash
from db import obtener_conexion

import mysql.connector

def registrar_usuario(correo, contraseña, nombre, telefono, direccion, fecha_nacimiento):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO usuario (correo, password_hash) VALUES (%s, %s)",
            (correo, generate_password_hash(contraseña,))
        )
        id_usuario = cursor.lastrowid
       
        
            
        # INSERT en Usuario_Detalle con id_usuario
        
        cursor.execute(
            "INSERT INTO usuario_detalle (Usuario_idUsuario, nombre,telefono,direccion,fecha_nacimiento) VALUES (%s,%s,%s,%s,%s)",
            (id_usuario,nombre,telefono,direccion,fecha_nacimiento,)
        )
        # INSERT en Billetera con id_usuario
       
        
        
        cursor.execute(
            "INSERT INTO billetera (Usuario_idUsuario) VALUES (%s)",
            (id_usuario,)
        )

        conexion.commit()
        return id_usuario
    except mysql.connector.Error as e:
        print(f"Error detectado {e}")
        conexion.rollback()
        print("Se ha descartado los cambios")
    finally:
        cursor.close()
        conexion.close()

