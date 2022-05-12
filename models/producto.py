from connection import Connection as db
from JsonEncoder import CustomJsonEncoder
import json

class Producto():
    def __init__(self, id=None, nombre=None, precio=None, categoria_id=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria_id = categoria_id

    def listar(self):
        cursor = db().open.cursor()
        cursor.execute('SELECT p.id, p.nombre AS producto, c.nombre AS categoria, p.precio FROM producto p INNER JOIN categoria c ON (p.categoria_id = c.id) ORDER BY p.nombre')
        datos = cursor.fetchall()
        cursor.close()
        if datos:
            return json.dumps({"status":True, "data":datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({"status":False, "data":"No hay datos"})

    def listarProductoTransaccion(self):
        cursor = db().open.cursor()
        cursor.execute('SELECT id, nombre from producto order by 2')
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

        #Prepapar la sentencia SQL Insert
        sql = "insert into producto (nombre,precio,categoria_id) values (%s,%s,%s)"

        try:
            # Ejecutar el comando SQL
            cursor.execute(sql, [self.nombre, self.precio, self.categoria_id])

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


    def leer(self, id):
        # Abrir conexión a la base de datos
        con = db().open

        # Crear un cursor
        cursor = con.cursor()

        # Se ejecuta la consulta SQL
        cursor.execute('select * from producto where id=%s', [id])

        # Capturar los datos
        datos = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        # Retonar el resultado
        if datos:
            return json.dumps({"status":True, "data":datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({"status":False, "data":"No hay datos"})


    def editar(self):
        # Abrir conexión a la base de datos
        con = db().open

        # Indicar que los cambios realizados en la base de datos no se confirman de manera automática
        con.autocommit = False

        # Crear un cursor
        cursor = con.cursor()

        #Prepapar la sentencia SQL Insert
        sql = "update producto set nombre=%s, precio=%s, categoria_id=%s where id=%s"

        try:
            # Ejecutar el comando SQL
            cursor.execute(sql, [self.nombre, self.precio, self.categoria_id, self.id])

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

    
    def eliminar(self, id):
        # Abrir conexión a la base de datos
        con = db().open

        # Indicar que los cambios realizados en la base de datos no se confirman de manera automática
        con.autocommit = False

        # Crear un cursor
        cursor = con.cursor()

        #Prepapar la sentencia SQL Insert
        sql = "delete from producto where id=%s"

        try:
            # Ejecutar el comando SQL
            cursor.execute(sql, [id])

            # Confirmar los cambios en la base datos
            con.commit()

            # Retorna un mensaje satisfactorio
            return json.dumps({"status":True, "data":"Eliminado satisfactoriamente"})
            
        except con.Error as error:
            # Revoca los cambios de la base de datos
            con.rollback()
            
            # Retorna un mensaje de error
            return json.dumps({"status":False, "data":format(error)}, cls=CustomJsonEncoder)
            
        finally:
            cursor.close()
            con.close()