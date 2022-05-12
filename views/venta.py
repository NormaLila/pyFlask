from flask import Blueprint, render_template, request, session, redirect, url_for, flash
#from models.categoria import Categoria
from models.venta import Venta
from models.tipoComprobante import TipoComprobante
from models.serie import Serie
from models.cliente import Cliente
from models.producto import Producto
from models.configuracion import Configuracion
import json
from datetime import date

view_venta = Blueprint('view_venta', __name__, template_folder='templates', static_folder='static')

@view_venta.route('/ventas')
def ventas():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        objVenta = Venta() #Instanciar la clase Venta
        rptaJSON = objVenta.listar()
        datosVenta = json.loads(rptaJSON)
        return render_template('venta-listar.html', datos=session, ventas=datosVenta)
    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_venta.route('/ventas/add')
def ventas_add():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        #Obtiene la lista de tipos de comprobante
        objTC = TipoComprobante()
        rptaJSON = objTC.listarTCVenta()
        datos_tc = json.loads(rptaJSON)

        #obtener fecha actual del servidor web
        today = date.today()
        fvta = today.strftime("%Y-%m-%d") #2021-05-03


        #Obtiene la lista de clientes
        objCliente = Cliente()
        rptaJSON = objCliente.listarClienteVenta()
        datos_cli = json.loads(rptaJSON)

        #Obtiene la lista de productos
        objProducto = Producto()
        rptaJSON = objProducto.listarProductoTransaccion()
        datos_prod = json.loads(rptaJSON)

        #Obtiene el porcentaje de IGV
        objConf = Configuracion()
        rptaJSON = objConf.obtenerValorConfiguracion('PORIGV')
        porc_igv = json.loads(rptaJSON)
        

        return render_template('venta-agregar.html', datos=session, tipos_comprobante=datos_tc, fecha_venta=fvta, clientes=datos_cli, productos=datos_prod, porc_igv=porc_igv)
    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_venta.route('/ventas/get/serie', methods=['POST'])
def ventas_get_serie():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        if request.method == 'POST':
            #Recibir el tipo de comprobante
            tc_id = request.form['tc_id']

            #Obtiene la lista de series según el tipo de comprobante seleccionado
            objSerie = Serie()
            rptaJSON = objSerie.listarSerie(tc_id)
            datos_serie = json.loads(rptaJSON)
            return datos_serie

    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))

@view_venta.route('/ventas/get/correlativo', methods=['POST'])
def ventas_get_correlativo():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        if request.method == 'POST':
            #Recibir la serie
            serie_nro = request.form['serie_nro']

            #Obtiene el correlativo para la serie
            objSerie = Serie()
            rptaJSON = objSerie.correlativo(serie_nro)
            correlativo = json.loads(rptaJSON)
            return correlativo

    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_venta.route('/ventas/save', methods=['POST'])
def ventas_save():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        if request.method == 'POST':
            #Recibir los datos de la venta
            cliente_id = request.form['cbocliente']
            tipo_comprobante_id = request.form['cbotc']
            nser = request.form['cboserie']
            ndoc = request.form['txtndoc']
            fdoc = request.form['txtfdoc']
            sub_total = request.form['txtsubtotal']
            igv = request.form['txtigv']
            total = request.form['txttotalneto']
            porcentaje_igv = request.form['txtporcentajeigv']
            usuario_id_registro = session["id"]
            
            #Recibir los datos del detalle de la venta (vienen en formato JSON)
            detalle = request.form['txtdetalleventa']

            #Instanciar al objeto objVta de la clase Venta y enviar los datos a grabar
            objVta = Venta(0, cliente_id, tipo_comprobante_id, nser, ndoc, fdoc, sub_total, igv, total, porcentaje_igv, usuario_id_registro, detalle)
            rptaJSON = objVta.insertar()
            datos_venta = json.loads(rptaJSON)

            # Imprimir el mensaje en pantalla
            flash(datos_venta['data'])

            # Llamar a la ruta '/ventas'
            return redirect(url_for('view_venta.ventas'))

    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_venta.route('/ventas/cancel/<id>')
def ventas_cancel(id):
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        #Instanciar la clase Venta
        objVenta = Venta()
        rptaJSON = objVenta.anular(session["id"], id)
        datos_venta = json.loads(rptaJSON)

        # Imprimir el mensaje en pantalla
        flash(datos_venta['data'])

        # Llamar a la rura '/productos'
        return redirect(url_for('view_venta.ventas'))

    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))