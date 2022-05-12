from flask import Flask, redirect, url_for

# Módulos de la aplicación web
from views.sesion import view_sesion
from views.producto import view_producto
from views.venta import view_venta

# Módulos del servicio web
from ws.sesion import ws_sesion
from ws.producto import ws_producto
from ws.venta import ws_venta
app = Flask(__name__)

#Crear una clave para la gestión de las sesiones de usuario
app.secret_key = "mycretetkey"

#Registrar los modulos de la aplicación python
app.register_blueprint(view_sesion)
app.register_blueprint(view_producto)
app.register_blueprint(view_venta)
app.register_blueprint(ws_producto)

#Registrar los módulos del servicio web
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_producto)
app.register_blueprint(ws_venta)

@app.route('/')
def home():
    return redirect(url_for('view_sesion.login'))

if __name__ == '__main__':
    app.run(port=3005, debug=True)