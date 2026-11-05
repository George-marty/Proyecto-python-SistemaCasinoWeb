from db import obtener_conexion
import mysql.connector

def ingresar_tarjeta(tipo, numero_tarjeta, fecha_vencimiento, id_Usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO tarjeta (tipo,numero_tarjeta,fecha_vencimiento,Usuario_idUsuario) VALUES (%s,%s,%s,%s)",
            (tipo, numero_tarjeta, fecha_vencimiento, id_Usuario)
        )
        idTarjetas = cursor.lastrowid
        conexion.commit()
        return idTarjetas
    except mysql.connector.Error as e:
        print(f"Error detectado {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()
    