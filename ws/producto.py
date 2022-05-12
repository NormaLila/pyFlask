from flask import Blueprint, request, jsonify
from models.producto import Producto
import json 
import validarJWT

ws_producto = Blueprint('ws_producto', __name__)

@ws_producto.route('/productos/ws', methods=['POST'])
# Funcion envoltura
@validarJWT.token_requerido
def productos_ws():
    objP = Producto()
    rptaJSON = objP.listar()
    datosP = json.loads(rptaJSON)

    # Imprime la lista de productos, indicando 200(ok) como resultado
    return jsonify(datosP), 200

@ws_producto.route('/productos/save/ws', methods=['POST'])
# Funcion envoltura
@validarJWT.token_requerido #Permite validar el token
def productos_save_ws():
    if request.method == 'POST':
        # Captura de datos del formulario
        id = request.form['id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria_id']

        # Instancia el objeto de la clase Producto y ejecuta los métodos    
        objP = Producto(id, nombre, precio, categoria_id)

        if id =='0':
            # Llamar al método insertar
            rptaJSON = objP.insertar()
        else:
            # Llamar al método editar
            rptaJSON = objP.editar()

        # Convertir el resultado JSON String JSON Array
        datosP = json.loads (rptaJSON) 

        #Imprimir el resultado de la operación (insertar/editar)
        if datosP['status'] == True:
            return jsonify(datosP), 200
        else:
            return jsonify(datosP), 500

@ws_producto.route('/productos/read/ws', methods=['POST'])
# Funcion envoltura
@validarJWT.token_requerido #Permite validar el token
def productos_read_ws():
    if request.method == 'POST':
        # Captura de datos del WS
        id = request.form['id']   

        #Obtiene los datos del producto a editar
        objP = Producto()
        rptaJSON = objP.leer(id)
        datos_prod = json.loads(rptaJSON)

        return jsonify(datos_prod), 200

@ws_producto.route('/productos/delete/ws', methods=['POST'])
# Funcion envoltura
@validarJWT.token_requerido #Permite validar el token
def productos_delete_ws():
    if request.method == 'POST':
        # Captura de datos del WS
        id = request.form['id']   

        #Obtiene los datos del producto a editar
        objP = Producto()
        rptaJSON = objP.eliminar(id)
        datos_prod = json.loads(rptaJSON)

        return jsonify(datos_prod), 200