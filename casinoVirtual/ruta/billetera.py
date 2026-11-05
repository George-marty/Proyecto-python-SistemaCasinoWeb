from flask import Blueprint, render_template, request, redirect, url_for, session
from modelo.billeteras import obtener_dato_user_wallet
from modelo.tarjeta import ingresar_tarjeta
from servicio.validaciones import convertir_vencimiento,numero_tarjeta_valido,tarjeta_vigente
billetera = Blueprint('billetera',__name__)

@billetera.route('/panel')
def panel():
    id_usuario = session.get('idUsuario')
    if id_usuario is None:
        return redirect(url_for('auth.login'))
    
    # 1. Llamamos a tu función para consultar MySQL con el ID de la sesión
    datos_usuario = obtener_dato_user_wallet(id_usuario)
    
    # 2. Pasamos el diccionario con el nombre 'usuario' que espera el HTML
    return render_template("panel.html", usuario=datos_usuario)

@billetera.route('/tarjeta',methods=['GET','POST'])
def tarjeta():
    id_usuario = session.get('idUsuario')
    
    if id_usuario is None:
        return redirect(url_for('billetera.panel'))
    if request.method == 'POST':
        tipo = request.form['tipo']
        numero_tarjeta = request.form['numero_tarjeta']
        fecha_vencimiento = convertir_vencimiento(request.form['fecha_vencimiento'])

        if tipo not in ("VISA", "MASTERCARD") or not numero_tarjeta_valido(numero_tarjeta) or not tarjeta_vigente(fecha_vencimiento):
            return render_template('tarjeta.html', error="Datos de tarjeta inválidos")

        id_tarjeta = ingresar_tarjeta(tipo, numero_tarjeta, fecha_vencimiento, id_usuario)
        return redirect(url_for('billetera.panel'))
    return render_template('tarjeta.html')