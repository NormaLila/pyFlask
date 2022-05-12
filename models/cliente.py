from connection import Connection as db
import json

class Cliente():
    def __init__(self):
        self = None
    
    def listarClienteVenta(self):
        cursor = db().open.cursor()
        cursor.execute('select * from cliente order by nombre')
        datos = cursor.fetchall()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos})
        else:
            return json.dumps({"status":False, "data":"No hay datos"})