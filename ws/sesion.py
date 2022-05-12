from flask import Blueprint, request, jsonify
from models.sesion import Sesion
import json
import utils
import jwt
import datetime
from config import SecretKey

ws_sesion = Blueprint('ws_sesion', __name__)

@ws_sesion.route('/login/auth/ws', methods=['POST'])
def auth_ws():

    if request.method == 'POST':
        email = request.form['email']
        clave = request.form['clave']

        objSesion = Sesion(email, clave)
        rptaJSON = objSesion.iniciarSesion()
        datos = json.loads(rptaJSON) #Convetir el JSON a un Array

        if datos["status"] == True: #Ha iniciado correctamente la sesión
            # Generando un Token
            # Obtener nel ID del usuario para ser almacenado en el token
            usuario_id = datos['data']['id']

            #Generar el token y almamacenar en la variable token
            token = jwt.encode({'usuario_id': usuario_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=4*60*60)}, SecretKey.JWT_SECRET_KEY)
            
            #Almacenar el token en la base de datos
            objSesion.actualizarToken(token, usuario_id)

            #Agregar el Token al resultado que devolverá al servicio web
            datos['data']['token'] = token.encode().decode('UTF-8')

            # Imprimir el resultado del servicio web
            return jsonify(datos), 200

        else: # Ocurrio un error en el inicio de sesión
            return jsonify(datos), 401
            
