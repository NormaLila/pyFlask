from flask import Blueprint, render_template, request, session, redirect, url_for
from models.sesion import Sesion
import json
import utils

view_sesion = Blueprint('view_sesion', __name__, template_folder='templates', static_folder='static')

@view_sesion.route('/login')
def login():
    return render_template('login.html')

@view_sesion.route('/login/auth', methods=['POST'])
def auth():

    if request.method == 'POST':
        email = request.form['txtemail']
        clave = request.form['txtclave']

        objSesion = Sesion(email, utils.md5_password(clave))
        rptaJSON = objSesion.iniciarSesion()
        datos = json.loads(rptaJSON) #Convetir el JSON a un Array

        if datos["status"] == True: #Ha iniciado correctamente la sesión
            #Crear la sesión del usuario
            session["nombre"] = datos["data"]["nombre"]
            session["email"] = datos["data"]["email"]
            session["id"] = datos["data"]["id"]
            session["img"] = datos["data"]["img"]
            return redirect(url_for('view_sesion.main'))
        else:
            return render_template ('login.html')


@view_sesion.route('/main')
def main():
    if "nombre" in session: #Significa que si ha iniciado sesión
        return render_template('menu.html', datos=session)
    else: #No ha iniciado sesión
        return redirect(url_for('view_sesion.login'))


@view_sesion.route('/logout')
def logout():
    session.pop("nombre", None)
    session.pop("email", None)
    session.pop("id", None)
    session.pop("img", None)
    return redirect(url_for('view_sesion.login'))