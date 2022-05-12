from connection import Connection as db
from JsonEncoder import CustomJsonEncoder
import json

class Venta():
    def __init__(self, id=None, cliente_id=None, tipo_comprobante_id=None, nser=None, ndoc=None, fdoc=None, sub_total=None, igv=None, total=None, porcentaje_igv=None, usuario_id_registro=None, detalle=None):
        self.id = id
        self.cliente_id = cliente_id
        self.tipo_comprobante_id = tipo_comprobante_id
        self.nser = nser
        self.ndoc = ndoc
        self.fdoc = fdoc
        self.sub_total = sub_total
        self.igv = igv
        self.total = total
        self.porcentaje_igv = porcentaje_igv
        self.usuario_id_registro = usuario_id_registro
        self.detalle = detalle
    
    def listar(self):
        cursor = db().open.cursor()
        cursor.execute('SELECT * from vista_venta_lista')
        datos = cursor.fetchall()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({"status":False, "data":"No hay datos"})


    def insertar(self):
        # Abrir conexión a la base de datos
        con = db().open

        # Indicar que los cambios realizados en la base de datos no se confirman de manera automática
        con.autocommit = False

        # Crear un cursor
        cursor = con.cursor()

        #Prepapar la sentencia SQL Insert (Tabla:venta)
        sql = "insert into venta (cliente_id,tipo_comprobante_id,nser,ndoc,fdoc,sub_total,igv,total,porcentaje_igv,usuario_id_registro) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            # Ejecutar el comando SQL (Tabla:venta)
            cursor.execute(sql, [self.cliente_id, self.tipo_comprobante_id, self.nser, self.ndoc, self.fdoc, self.sub_total, self.igv, self.total, self.porcentaje_igv, self.usuario_id_registro])

            #Obtener el id de la venta para insertarlo en la tabla venta_detalle
            self.id = con.insert_id()

            #Grabar en la Tabla:venta_detalle
            #Recoger el JSON del detalle de la venta y colocarlo con JSON Array
            jsonArrayVentaDetalle = json.loads(self.detalle)

            #Recorrer los elementos del Array jsonArrayVentaDetalle
            for det in jsonArrayVentaDetalle:
                #Prepapar la sentencia SQL Insert (Tabla:venta_detalle)
                sql = "insert into venta_detalle (venta_id,producto_id,cantidad,precio) values (%s,%s,%s,%s)"
                
                # Ejecutar el comando SQL (Tabla:venta)
                cursor.execute(sql, [self.id, det["producto_id"], det["cantidad"], det["precio"]])

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
    

    def anular(self, usuario_id_anulacion, id):
        # Abrir conexión a la base de datos
        con = db().open

        # Indicar que los cambios realizados en la base de datos no se confirman de manera automática
        con.autocommit = False

        # Crear un cursor
        cursor = con.cursor()

        #Prepapar la sentencia SQL Insert
        sql = "update venta set estado='0', usuario_id_anulacion=%s, fecha_hora_anulacion=NOW() where id=%s"

        try:
            # Ejecutar el comando SQL
            cursor.execute(sql, [usuario_id_anulacion, id])

            # Confirmar los cambios en la base datos
            con.commit()

            # Retorna un mensaje satisfactorio
            return json.dumps({"status":True, "data":"Venta anulada satisfactoriamente"})
            
        except con.Error as error:
            # Revoca los cambios de la base de datos
            con.rollback()
            
            # Retorna un mensaje de error
            return json.dumps({"status":False, "data":format(error)}, cls=CustomJsonEncoder)
            
        finally:
            cursor.close()
            con.close()

