import mysql.connector
from config import configuracion

def obtener_conexion():
    return mysql.connector.connect(**configuracion())