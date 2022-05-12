from connection import Connection as db
import json

class Configuracion():
    def __init__(self):
        self = None
    
    def obtenerValorConfiguracion(self, id):
        cursor = db().open.cursor()
        cursor.execute('select valor from configuracion where id=%s',[id])
        datos = cursor.fetchone()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos})
        else:
            return json.dumps({"status":False, "data":"No hay datos"})