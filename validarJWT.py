from flask import jsonify, request
import jwt
from functools import wraps
from config import SecretKey
import json

from models.sesion import Sesion

def token_requerido(f): #Funcion de envoltura para validar el token
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.args.get('token') #http://127.0.0.1:5000/route?token=xyz.token
        token = request.form['token']

        if not token:
            return jsonify({'status':False,'data' : 'No hay token'}), 403
        try: 
            data = jwt.decode(token, SecretKey.JWT_SECRET_KEY, algorithms=["HS256"])
            print('==========usuario_id:'+format(data['usuario_id']))

            estado_token = validar_estado_token(data['usuario_id'])
            if estado_token == False:
                return jsonify({'status':False, 'data' : 'El token se encuentra inactivo'}), 403
            
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as error:
            return jsonify({'status':False, 'data' : 'El token es invalido', 'internal_error': format(error)}), 403
        
        except (Exception) as error:
            return jsonify({'status':False, 'data' : 'Error', 'internal_error': format(error)}), 403

        return f(*args, **kwargs)

    return decorated

def validar_estado_token(id):
    objSesion = Sesion()
    rptaJSON = objSesion.validarEstadoToken(id)
    datos_token = json.loads(rptaJSON)
    if datos_token['status'] == True:
        estado_token = datos_token['data']['estado_token']
        if estado_token==None:
            return False
        else:
            if estado_token=='0':
                return False
            else:
                return True
    else:
        return False
        





