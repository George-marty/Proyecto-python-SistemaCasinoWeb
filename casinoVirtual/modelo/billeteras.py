from db import obtener_conexion

def obtener_dato_user_wallet(usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT ud.nombre,b.saldo_virtual,b.saldo_casual,b.ultima_actualizacion
                FROM usuario AS u
                INNER JOIN usuario_detalle AS ud ON  u.idUsuario = ud.Usuario_idUsuario
                INNER JOIN billetera AS b ON u.idUsuario = b.Usuario_idUsuario
                WHERE idUsuario = %s """,(usuario,))
        if usuario is None:
            return None
        return cursor.fetchone()

    
    finally:
        cursor.close()
        conexion.close()

