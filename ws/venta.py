from flask import Blueprint, request, jsonify
from models.venta import Venta
import json 
import validarJWT

ws_venta = Blueprint('ws_venta', __name__)

@ws_venta.route('/ventas/save', methods=['POST'])
@validarJWT.token_requerido
def ventas_save_ws():
            
    if request.method == 'POST':
        #Recibir los datos de la venta
        cliente_id = request.form['cliente']
        tipo_comprobante_id = request.form['tc_id']
        nser = request.form['serie']
        ndoc = request.form['ndoc']
        fdoc = request.form['fdoc']
        sub_total = request.form['subtotal']
        igv = request.form['igv']
        total = request.form['totalneto']
        porcentaje_igv = request.form['porcentajeigv']
        usuario_id_registro = request.form["usuario_id_registro"]
        
        #Recibir los datos del detalle de la venta (vienen en formato JSON)
        detalle = request.form['detalleventa']

        #Instanciar al objeto objVta de la clase Venta y enviar los datos a grabar
        objVta = Venta(0, cliente_id, tipo_comprobante_id, nser, ndoc, fdoc, sub_total, igv, total, porcentaje_igv, usuario_id_registro, detalle)
        rptaJSON = objVta.insertar()
        datos_venta = json.loads(rptaJSON)

       #Imprimir resultados de la operación (insertar venta)
        if datos_venta['status'] == True:
            return jsonify(datos_venta), 200
        else:
            return jsonify(datos_venta), 500
