from flask import Flask, render_template,request,redirect,url_for,session
from ruta.billetera import billetera
from config import SECRET_KEY
from ruta.auth import auth

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth)
app.register_blueprint(billetera)



@app.route('/')
def index():
  return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)