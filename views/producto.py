from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.producto import Producto
from models.categoria import Categoria
import json

view_producto = Blueprint('view_producto', __name__, template_folder='templates', static_folder='static')

@view_producto.route('/productos')
def productos():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        objP = Producto()
        rptaJSON = objP.listar()
        datosP = json.loads(rptaJSON)
        return render_template('producto-listar.html', datos=session, productos=datosP)
    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))

@view_producto.route('/productos/add')
def productos_add():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        #Obtiene la lista de categorías para el combo cbocategoria
        objCat = Categoria()
        rptaJSON = objCat.listar()
        datos_cat = json.loads(rptaJSON)

        return render_template('producto-agregar-editar.html', datos=session, categorias=datos_cat)
    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_producto.route('/productos/save', methods=['POST'])
def productos_save():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        if request.method == 'POST':
            # Captura de datos del formulario
            id = request.form['txtid']
            nombre = request.form['txtnombre']
            precio = request.form['txtprecio']
            categoria_id = request.form['cbocategoria']

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

            # Imprimir el mensaje en pantalla
            flash(datosP['data'])

            # Llamar a la rura '/productos'
            return redirect(url_for('view_producto.productos'))



    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_producto.route('/productos/edit/<id>')
def productos_edit(id):
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        #Obtiene la lista de categorías para el combo cbocategoria
        objCat = Categoria()
        rptaJSON = objCat.listar()
        datos_cat = json.loads(rptaJSON)

        #Obtiene los datos del producto a editar
        objP = Producto()
        rptaJSON = objP.leer(id)
        datos_prod = json.loads(rptaJSON)

        return render_template('producto-agregar-editar.html', datos=session, categorias=datos_cat, producto=datos_prod)
    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_producto.route('/productos/delete/<id>')
def productos_delete(id):
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        #Instanciar la clase producto
        objP = Producto()
        rptaJSON = objP.eliminar(id)
        datos_prod = json.loads(rptaJSON)

        # Imprimir el mensaje en pantalla
        flash(datos_prod['data'])

        # Llamar a la rura '/productos'
        return redirect(url_for('view_producto.productos'))

    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))


@view_producto.route('/productos/get/data', methods=['POST'])
def productos_get_data():
    if "nombre" in session: #Significa que el usuario si ha iniciado sesión
        
        if request.method == 'POST':
            #Recibir el producto_id
            producto_id = request.form['producto_id']

            #Obtiene los datos del producto según su ID
            objProducto = Producto()
            rptaJSON = objProducto.leer(producto_id)
            datos_prod = json.loads(rptaJSON)
            return datos_prod

    else: #No ha inciado sesión
        return redirect(url_for('view_sesion.login'))