from connection import Connection as db
import json

class TipoComprobante():
    def __init__(self):
        self = None
    
    def listarTCVenta(self):
        cursor = db().open.cursor()
        cursor.execute("select * from tipo_comprobante where venta = '1' order by nombre")
        datos = cursor.fetchall()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos})
        else:
            return json.dumps({"status":False, "data":"No hay datos"})