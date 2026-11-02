from flask import Flask, render_template,request,redirect,url_for,session
from config import SECRET_KEY
from ruta.auth import auth

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth)


@app.route('/panel')
def panel():
    id_usuario = session.get('idUsuario')
    if id_usuario is None:
        return redirect(url_for('auth.login'))
    return f'Hola, {id_usuario}'



if __name__=="__main__":
    app.run(debug=True)