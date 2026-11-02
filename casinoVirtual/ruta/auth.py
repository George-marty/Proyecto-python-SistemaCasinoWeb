from flask import Blueprint, render_template, request, redirect, url_for, session

from servicio.validaciones import es_mayor_edad
from servicio.registro import registrar_usuario
from modelo.usuario import verificar_login
from modelo.usuario import obtener_correo_usuario


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['password']
        usuario = verificar_login(correo, contraseña)
        if usuario:
            # guardar idUsuario y rol en session
            
            session['idUsuario'] = usuario['idUsuario']
            session['rol'] =  usuario['rol']
            
            return redirect(url_for('panel'))
        return render_template('login.html', error="Correo o contraseña incorrectos")
    return render_template('login.html')


@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fecha_nacimiento = request.form['fecha_nacimiento']
        if es_mayor_edad(fecha_nacimiento) is False:
            return render_template('register.html', error="no cumple con los requirimientos de edad")
        contraseña = request.form['password']
        correo = request.form['correo']
        if obtener_correo_usuario(correo) is not None:
            return render_template('register.html', error="El correo ya esta registrado")
        
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        
        
        
        usuario = registrar_usuario(correo, contraseña, nombre, telefono, direccion, fecha_nacimiento)
        if usuario is  None:
            return render_template('register.html',error="No se pudo registrar usuario")
        return redirect(url_for('auth.login'))

            
    return render_template('register.html')

@auth.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for('auth.login'))