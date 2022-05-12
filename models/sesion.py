from connection import Connection as db
from JsonEncoder import CustomJsonEncoder
import json

class Sesion():
    def __init__(self, p_email=None, p_clave=None):
        self.email = p_email
        self.clave = p_clave

    def iniciarSesion(self):
        cursor = db().open.cursor()
        cursor.execute('select id, nombre, email, img, estado_usuario from usuario where email = %s and clave = %s', [self.email, self.clave])
        datos = cursor.fetchone()
        cursor.close()
        if datos:
            # Validar si el usuario tiene estado activo
            if datos['estado_usuario'] == '1': #1 = activo
                return json.dumps({"status":True, "data":datos})
            else:
                return json.dumps({"status":True, "data":"usuario inactivo"})
        else:
            return json.dumps({"status":False, "data":"Email o clave son incorrectos"})

    def actualizarToken(selt, token, id):
        # Abrir conexión a la base de datos
        con = db().open

        # Indicar que los cambios realizados en la base de datos no se confirman de manera automática
        con.autocommit = False

        # Crear un cursor
        cursor = con.cursor()

        #Prepapar la sentencia SQL Insert
        sql = "update producto set tiken=%s, estado_token='1'%s, where id=%s"

        try:
            # Ejecutar el comando SQL
            cursor.execute(sql, [token, id])

            # Confirmar los cambios en la base datos
            con.commit()

            # Retorna un mensaje satisfactorio
            return json.dumps({"status":True, "data":"Grabado satisfactoriamente"})
            
        except con.Error as error:
            # Revoca los cambios de la base de datos
            con.rollback()
            
            # Retorna un mensaje de error
            return json.dumps({"status":False, "data":format(error)}, cls=CustomJsonEncoder)
            
        finally:
            cursor.close()
            con.close()

    def validarEstadoToken(self, id):
        # Abrir conexi�n a la base de datos
        con = db().open

        # Crear un cursor
        cursor = con.cursor()

        # Se ejecuta la consulta SQL
        cursor.execute('select estado_token from usuario where id = %s', [id])

        # Capturar los datos
        datos = cursor.fetchone()

        # Cerrar el cursor y la conexi�n
        cursor.close()
        con.close()

        # Retonar el resultado
        if datos:
            return json.dumps({"status":True, "data":datos})
        else:
            return json.dumps({"status":False, "data":"Estado de token no encontrado"})