from connection import Connection as db
import json

class Serie():
    def __init__(self):
        self = None
    
    def listarSerie(self, tipo_comprobante_id):
        cursor = db().open.cursor()
        cursor.execute("select serie from serie where tipo_comprobante_id = %s order by serie", [tipo_comprobante_id])
        datos = cursor.fetchall()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos})
        else:
            return json.dumps({"status":False, "data":"No hay datos"})


    def correlativo(self, serie_nro):
        cursor = db().open.cursor()
        cursor.execute("select ndoc+1 as corre from serie where serie = %s", [serie_nro])
        datos = cursor.fetchone()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos})
        else:
            return json.dumps({"status":False, "data":"No hay datos"})

