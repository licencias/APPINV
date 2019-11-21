from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import date


#INITIALIZATION
app = Flask(__name__)

#MYSQL CONECTION
app.config['MYSQL_HOST'] = 'NetAxion.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'NetAxion'
app.config['MYSQL_PASSWORD'] = 'casa89403670'
app.config['MYSQL_DB'] = 'NetAxion$db3'
mysql = MySQL(app)


#SETTINGS
app.secret_key = "mysecretkey"

#404
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

#URLS
@app.route('/formulario_factura')
def formulario_factura():
    return render_template('formulario_factura.html')

@app.route('/formulario_mostrar_componentes')
def formulario_mostrar_componentes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM NetAxion$db5.registro_componente')
    data = cur.fetchall()
    cur.close()
    return render_template('formulario_mostrar_componentes.html',datos = data)

@app.route('/tabla_mert_produccion')
def tabla_mert_produccion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM NetAxion$db5.mert_produccion')
    data = cur.fetchall()
    cur.close()

    return render_template('tabla_mert_produccion.html',datos = data)

@app.route('/tabla_mert_inventario')
def tabla_mert_inventario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM NetAxion$db5.mert')
    data = cur.fetchall()
    cur.close()

    return render_template('tabla_mert_inventario.html',datos = data)

@app.route('/qa_pic')
def qa_pic():
    return render_template('qa_pic.html')

@app.route('/qa_mert')
def qa_mert():
    return render_template('qa_mert.html')

@app.route('/formulario_componente')
def formulario_componente():
    return render_template('formulario_componente.html')

@app.route('/formulario_mert_produccion')
def formulario_mert_produccion():
    return render_template('formulario_mert_produccion.html')

@app.route('/formulario_mert')
def formulario_mert():
    return render_template('formulario_mert.html')

@app.route('/formulario_pic')
def formulario_pic():
    return render_template('formulario_pic.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario_no_encontrado')
def usuario_no_encontrado():
    return render_template('usuario_no_encontrado.html')

@app.route('/formulario_mostrar')
def formulario_mostrar():
    return render_template('formulario_mostrar.html')

@app.route('/formulario_modificar')
def formulario_modificar():
    return render_template('formulario_modificar.html')

#FORMULARIOS

@app.route('/form_prod',methods=['POST'])
def form_prod():
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute('UPDATE NetAxion$db5.mert SET disponibilidad = 0 WHERE serial_salida = {}'.format(request.form['serie_origen']))
        mysql.connection.commit() 
        
        cur.execute('insert into NetAxion$db5.mert_produccion (nombre_cliente,faena,fecha_salida, serial_salida,flota_destino) values (%s,%s,%s,%s,%s)',(request.form['nombre'],request.form['faena'],request.form['fecha'],request.form['serial'],request.form['flota']))
        mysql.connection.commit()        
        cur.close()
        return render_template('formulario_mert_produccion.html')

@app.route('/formulario_comp',methods = ['POST'])
def formulario_comp():
    if(request.method == 'POST'):
        serial = request.form['serial']
        nombre = request.form['nombre']
        rut = request.form['rut']
        qa = request.form['radio']
        id_usuario = request.form['id_usuario']
        fecha = date.today()
        tipo_producto = "componente"
        estado_disponibilidad = 0
        if(int(qa) == 1):
            estado_disponibilidad = 1
        #usuario
        cur = mysql.connection.cursor()
        cur.execute('insert into NetAxion$db5.usuario (nombre,rut) values (%s,%s)', (nombre,rut))
        mysql.connection.commit()

        #query's select
        user = cur.execute('SELECT * FROM NetAxion$db5.usuario')
        if(int(id_usuario) <= int(user) and int(id_usuario) >= 0):
            id_usuario = request.form['id_usuario']
        else:
            return render_template('usuario_no_encontrado.html')

        #registro_componente
        cur.execute('UPDATE NetAxion$db5.registro_componente SET quality_assurance= %s, fecha_produccion = %s, id_usuario= %s, tipo_producto = %s, estado_disponibilidad = %s WHERE  id_registro_componente=%s', (qa,fecha,id_usuario,tipo_producto,estado_disponibilidad,serial))
        mysql.connection.commit()

        cur.close()
        return render_template('formulario_componente.html')#, componentes = data

@app.route('/form_qa_mert', methods=['POST'])
def form_qa_mert():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        if(int(request.form['radio']) == 1):
            cur.execute('UPDATE NetAxion$db5.mert SET qa = 1, disponibilidad = 1, id_registro_componente = 1 WHERE serial_salida = {}'.format(request.form['serial']))
            mysql.connection.commit()

        cur.close()
        return render_template('qa_mert.html')
 
@app.route('/form_mert', methods=['POST'])
def form_mert():
    if request.method == 'POST':
        #listar componententes
        cur = mysql.connection.cursor()
        sql = "select * from NetAxion$db5.registro_componente"
        cur.execute(sql)
        print(cur.fetchone())
        #conexion a base de datos
        qa = 0
        cur = mysql.connection.cursor() 
        cur.execute('insert into NetAxion$db5.mert (rut_usuario, fecha_produccion, serial_salida, qa) values (%s,%s,%s,%s)', (request.form['nombre'], request.form['rut'], request.form['serial'],qa))
        mysql.connection.commit()
        cur.execute('SELECT * FROM NetAxion$db5.registro_componente ORDER BY nombre_producto')
        nombre_componente = "unstring"
        sql = cur.fetchall()
        for i in sql:
            if(i[8] == "1" and i[1] != nombre_componente):
                nombre_componente = i[2]
                print(i[0],i[1],i[2],i[3])
                print(request.form['serial'])
                cur.execute('update NetAxion$db5.registro_componente set estado_disponibilidad = 0, serie_premert = %s WHERE id_registro_componente = %s',(request.form['serial'],i[0]))
                mysql.connection.commit()
        cur.close()

        return render_template('index.html')
    
@app.route('/formulario',methods = ['POST'])
def formulario():
    if(request.method == 'POST'):
        print("xD")
    return render_template('formulario_pic.html')

@app.route('/formulario_proveedor', methods=['POST'])
def formulario_proveedor():
    if request.method == 'POST':
        #conexion a base de datos
        cur = mysql.connection.cursor() 
        cur.execute('insert into NetAxion$db5.factura (nombre_proveedor, rut_proveedor) values (%s,%s)', (request.form['nombre_proveedor'], request.form['rut_proveedor']))
        mysql.connection.commit()
        sll = cur.execute('select * FROM NetAxion$db5.factura')
        id_factura = sll
        cur.execute('insert into NetAxion$db5.detalle_factura (id_factura, nombre_producto, fecha_factura, cantidad, precio_neto, iva, precio_total) values (%s,%s,%s,%s,%s,%s,%s)', (id_factura, request.form['nombre_producto'], request.form['fecha_factura'], request.form['cantidad'], request.form['valor_neto'], request.form['iva'], request.form['valor_total']))
        mysql.connection.commit()
        if(int(request.form['cantidad']) >= 1):
            for i in range(int(request.form['cantidad'])):
                cur.execute('insert into NetAxion$db5.registro_componente (nombre_producto) values (%s)',(request.form['nombre_producto'],))
                print(request.form['nombre_producto'])
                mysql.connection.commit()
        cur.close()

        return render_template('formulario_factura.html')

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_mert_inventario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM NetAxion$db5.mert WHERE id_mert = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))
    
@app.route('/delete2/<string:id>', methods = ['POST','GET'])
def delete2_mert_inventario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM NetAxion$db5.mert_produccion WHERE id_mert_produccion = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM NetAxion$db5.mert WHERE id_mert = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('editar.html', mert = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_mert(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE NetAxion$db5.mert
            SET rut_usuario = %s,
                fecha_produccion = %s,
                serial_salida = %s,
                qa = %s
            WHERE id_mert = %s
        """, (request.form['rut'], request.form['fecha'], request.form['serial'],request.form['radio'], id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/edit2/<id>', methods = ['POST', 'GET'])
def get_contact2(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM NetAxion$db5.mert_produccion WHERE id_mert_produccion = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('editar2.html', mert = data[0])

@app.route('/update2/<id>', methods=['POST'])
def update_mert_produccion(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE NetAxion$db5.mert_produccion
            SET descripcion = %s,
                nombre_cliente = %s,
                faena = %s,
                fecha_salida = %s,
                serial_salida = %s,
                flota_destino = %s
            WHERE id_mert_produccion = %s
        """, (request.form['descripcion'], request.form['nombre'], request.form['faena'],request.form['fecha'],request.form['serial'],request.form['flota'], id, ))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/edit3/<id>', methods = ['POST', 'GET'])
def get_contact3(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM NetAxion$db5.registro_componente WHERE id_registro_componente = {0}'.format(id))#importante .format para que el indice pueda iterar en la base de datos
    data = cur.fetchall()
    cur.close()
    return render_template('editar3.html', componente = data[0])

@app.route('/update3/<id>', methods=['POST'])
def update_componente(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE NetAxion$db5.registro_componente
            SET quality_assurance = %s,
                fecha_produccion = %s
            
            WHERE id_registro_componente = %s
        """, (request.form['radio'], request.form['fecha'], int(id)))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=3000 ,debug=True)































































