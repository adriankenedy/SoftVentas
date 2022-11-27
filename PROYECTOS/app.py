from flask import Flask, render_template, request, session, flash
from flask_paginate import Pagination, get_page_parameter
from Datos.connection import connection
from datetime import date
import logging
import os
from mysql.connector import Error

logging.getLogger("werkzeug").disabled = True

app = Flask(__name__)

if not os.path.isdir('logs'):
    os.makedirs('logs')


logging.basicConfig(filename='logs/logs.log', filemode='w', level=logging.DEBUG)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

cursor = connection.cursor()
today = date.today()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inicio', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM usuario WHERE usuario = %s AND contrasenia = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        
        # If account exists in accounts table in out database
        if account:
            user = account[1]
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[3]
            session['username'] = account[4]
            # Redirect to home page
            return render_template('comunes/principal.html', user=user)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
            return render_template('index.html', msg=msg) 


@app.route('/cerrarsesion')
def cerrarsesion():
    return render_template('index.html')

@app.route('/menu')
def inicio():
    return render_template('comunes/principal.html')


#------------------------------------------------------- USUARIOS ------------------------------------------------------
#muestra la lista de usuarios

@app.route('/usuarios')
def Usuario():
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM usuario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM usuario ORDER BY idUsuario ASC LIMIT %s OFFSET %s', (per_page, offset))
    usuarios = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='usuarios')
    return render_template('usuario/usuarioLista.html', usuarios=usuarios, pagination=pagination)
    

#redirecciona para poder crear un nuevo usuario

@app.route('/nuevoUsuario')
def nuevoUsuario():
    return render_template('usuario/nuevoUsuario.html')

#crea/inserta un nuevo usuario

@app.route('/insertarUsuario', methods=['GET', 'POST'])
def agregarUsuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        password = request.form['password']
        cursor.execute('INSERT INTO usuario (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)'
                        ,(nombre, apellido, usuario, password))
        connection.commit()
    
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM usuario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM usuario ORDER BY idUsuario ASC LIMIT %s OFFSET %s', (per_page, offset))
    usuarios = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='usuarios')

    return render_template('usuario/usuarioLista.html', usuarios=usuarios, pagination=pagination)


#selecciona el usuario a editar

@app.route('/editarUsuario/<id>')
def editarDeduccion(id):
    cursor.execute(f'Select idUsuario, nombre, apellido, usuario, contrasenia from usuario where idUsuario={id}')
    user = cursor.fetchall()
    return render_template('usuario/editarUsuario.html', usuario = user[0])

#edita el usuario seleccionado

@app.route('/actualizarUsuario/<id>', methods=['GET','POST'])
def actualizarUsuario(id):
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM usuario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM usuario ORDER BY idUsuario ASC LIMIT %s OFFSET %s', (per_page, offset))
    usuarios = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='usuarios')

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        password = request.form['password']
    
        cursor.execute('Update usuario set nombre=%s, apellido=%s, usuario=%s, contrasenia=%s where idUsuario=%s'
        ,(nombre, apellido, usuario, password, id))
        connection.commit()
    return render_template('usuario/usuarioLista.html', usuarios=usuarios, pagination=pagination)


#elimina un usuario

@app.route('/eliminarUsuario/<string:id>')
def eliminarUsuario(id):
    cursor.execute(f'Delete from usuario where idUsuario={id}')
    connection.commit()

    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM usuario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM usuario ORDER BY idUsuario ASC LIMIT %s OFFSET %s', (per_page, offset))
    usuarios = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='usuarios')
    return render_template('usuario/usuarioLista.html', usuarios=usuarios, pagination=pagination)




#------------------------------------------------------ PRODUCTOS ------------------------------------------------------

@app.route('/inventario')
def Producto():
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM inventario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM inventario ORDER BY idInventario ASC LIMIT %s OFFSET %s', (per_page, offset))
    inventario = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='productos')
    
    return render_template('inventario/inventarioLista.html', pagination=pagination, inventario=inventario)


@app.route('/nuevoPInventario')
def nuevoProducto():
    return render_template('inventario/nuevoPInventario.html')


@app.route('/insertarPInventario', methods=['GET', 'POST'])
def insertarProducto():

    if request.method == 'POST':
        nombre = request.form['nombrePI']
        descripcion = request.form['descripcion']
        lote = request.form['lote']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        cursor.execute('INSERT INTO inventario (nombre, descripcion, lote, precio, cantidad) VALUES (%s, %s, %s, %s, %s)'
                        ,(nombre, descripcion, lote, precio, cantidad))
        connection.commit()

    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM inventario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM inventario ORDER BY idInventario ASC LIMIT %s OFFSET %s', (per_page, offset))
    inventario = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='productos')
    
    return render_template('inventario/inventarioLista.html', pagination=pagination, inventario=inventario)


@app.route('/editarInventario/<id>')
def editarPInventario(id):
    cursor.execute(f'Select idInventario, nombre, descripcion, lote, precio, cantidad from inventario where idInventario={id}')
    inventario = cursor.fetchall()
    return render_template('inventario/editarPInventario.html', inventario = inventario[0])


@app.route('/actualizarPInventario/<id>', methods=['GET', 'POST'])
def actualizarPInventario(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        lote = request.form['lote']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
    
        cursor.execute('Update inventario set nombre=%s, descripcion=%s, lote=%s, precio=%s, cantidad=%s where idInventario=%s'
        ,(nombre, descripcion, lote, precio, cantidad, id))
        connection.commit()

    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM inventario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM inventario ORDER BY idInventario ASC LIMIT %s OFFSET %s', (per_page, offset))
    inventario = cursor.fetchall()
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='productos')

    return render_template('inventario/inventarioLista.html', inventario=inventario, pagination=pagination)


@app.route('/eliminarInventario/<string:id>')
def eliminarInventario(id):
    cursor.execute(f'Delete from inventario where idInventario={id}')
    connection.commit()

    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM inventario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM inventario ORDER BY idInventario ASC LIMIT %s OFFSET %s', (per_page, offset))
    inventario = cursor.fetchall()
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='productos')

    return render_template('inventario/inventarioLista.html', inventario=inventario, pagination=pagination)





#--------------------------------------------------------- VENTAS ------------------------------------------------------

@app.route('/ventas')
def ventas():
    per_page = 100
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM inventario;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM inventario ORDER BY idInventario ASC LIMIT %s OFFSET %s', (per_page, offset))
    inventario = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='productos')
    
    return render_template('ventas/ventasLista.html', carrito=inventario, pagination=pagination)



@app.route('/terminarVenta', methods=['POST'])
def terminarVenta():
    try:
        if request.method == 'POST':
            ventas = []
            insertarVenta = 'INSERT INTO producto (nombre, lote, precio, cantidad, idVenta) VALUES (%s, %s, %s, %s, %s)'
            selectVenta = 'SELECT idVenta FROM Venta ORDER BY idVenta DESC LIMIT 1;'

            producto = request.form.getlist('producto')
            lote = request.form.getlist('lote')
            precio = request.form.getlist('precio')
            cantidad = request.form.getlist('cantidad')
            idinventario = request.form.getlist('id')
            sumatotal = request.form.get('sumaproductos')

            cursor.execute('INSERT INTO venta (fecha, total) VALUES (%s, %s)' ,(today, sumatotal))

            cursor.execute(selectVenta)
            venta = cursor.fetchone()

            ventas.append(venta)
            
            for v in ventas:
                logging.info(f'--------- Venta agregada: {v}')
                
                for i, prod in enumerate(producto):

                    lista = [
                        (prod, lote[i], precio[i], cantidad[i], ','.join(map(str, v)))
                    ]

                    args = (int(idinventario[i]), int(cantidad[i]))
                    cursor.callproc('apiActualizarInventario', args)

                    logging.info('------------------ Productos de la venta ------------------')
                    logging.info(f'{today}: {lista}')
            
                    cursor.executemany(insertarVenta, lista)

            connection.commit()


        per_page = 100
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = (page - 1) * per_page

        cursor.execute('SELECT *FROM inventario;')
        total = cursor.fetchall()

        cursor.execute('SELECT * FROM inventario ORDER BY idInventario ASC LIMIT %s OFFSET %s', (per_page, offset))
        inventario = cursor.fetchall()
        
        return render_template('ventas/ventasLista.html', carrito=inventario)

    except  Error as e:
        logging.error(f' Ocurrio un error en la venta: {e}')


#--------------------------------------------------------- REGISTROS ------------------------------------------------------

@app.route('/registros')
def registros():
    per_page = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor.execute('SELECT *FROM venta;')
    total = cursor.fetchall()

    cursor.execute('SELECT * FROM venta ORDER BY idVenta DESC LIMIT %s OFFSET %s', (per_page, offset))
    registros = cursor.fetchall()

    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='ventas')
    
    return render_template('registros/listaRegistros.html', registros=registros, pagination=pagination)



@app.route('/verRegistro/<id>')
def detalleRegistro(id):
    cursor.execute(f'Select nombre, lote, precio, cantidad from producto where idVenta={id}')
    detalles = cursor.fetchall()
    return render_template('registros/verRegistro.html', detalles = detalles)


if __name__ == '__main__':
    app.run(debug=True)