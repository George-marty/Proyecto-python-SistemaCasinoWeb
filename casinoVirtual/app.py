from flask import Flask, render_template,request,redirect,url_for,session
from config import SECRET_KEY
from modelo.usuario import verificar_login


app = Flask(__name__)
app.secret_key = SECRET_KEY



@app.route('/login', methods=['GET', 'POST'])
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
@app.route('/panel')
def panel():
    id_usuario = session.get('idUsuario')
    if id_usuario is None:
        return redirect(url_for('login'))
    return f'Hola, {id_usuario}'

@app.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)