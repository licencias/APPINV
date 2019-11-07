from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb

#INITIALIZATION
app = Flask(__name__)

#MYSQL CONECTION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'almacen_componentes'
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

#FORMULARIOS

@app.route('/form_prod',methods=['POST'])
def form_prod():
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute('UPDATE almacen_componentes.mert SET disponibilidad = 0 WHERE serial_salida = {}'.format(request.form['serie_origen']))
        mysql.connection.commit() 
        
        cur.execute('insert into mert_produccion (nombre_cliente,rut_cliente,fecha_salida, serial_salida,flota_destino) values (%s,%s,%s,%s,%s)',(request.form['nombre'],request.form['rut'],request.form['fecha'],request.form['serial'],request.form['flota']))
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
        cur.execute('insert into usuario (nombre,rut) values (%s,%s)', (nombre,rut))
        mysql.connection.commit()

        #query's select
        user = cur.execute('SELECT * FROM usuario')
        if(int(id_usuario) <= int(user) and int(id_usuario) >= 0):
            id_usuario = request.form['id_usuario']
        else:
            return render_template('usuario_no_encontrado.html')

        #registro_componente
        cur.execute('UPDATE almacen_componentes.registro_componente SET quality_assurance=%s, fecha_produccion = %s, id_usuario= %s, tipo_producto = %s, estado_disponibilidad = %s WHERE  id_registro_componente=%s', (qa,fecha,id_usuario,tipo_producto,estado_disponibilidad,serial))
        mysql.connection.commit()

        cur.close()
        return render_template('index.html')#, componentes = data

@app.route('/form_qa_mert', methods=['POST'])
def form_qa_mert():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        if(int(request.form['radio']) == 1):
            cur.execute('UPDATE almacen_componentes.mert SET qa = 1, disponibilidad = 1, id_registro_componente = 1 WHERE serial_salida = {}'.format(request.form['serial']))
            mysql.connection.commit()

        cur.close()
        return render_template('index.html')
 
@app.route('/form_mert', methods=['POST'])
def form_mert():
    if request.method == 'POST':
        #conexion a base de datos
        qa = 0
        cur = mysql.connection.cursor() 
        cur.execute('insert into mert (rut_usuario, fecha_produccion, serial_salida, qa) values (%s,%s,%s,%s)', (request.form['nombre'], request.form['rut'], request.form['serial'],qa))
        mysql.connection.commit()
        cur.execute('SELECT * FROM registro_componente')
        nombre_componente = "unstring"
        sql = cur.fetchall()
        for i in sql:
            if(i[7] == "1" and i[2] != nombre_componente):
                nombre_componente = i[2]
                cur.execute('UPDATE almacen_componentes.registro_componente SET estado_disponibilidad = 0 WHERE id_registro_componente = {}'.format(i[0]))
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
        cur.execute('insert into factura (nombre_proveedor, rut_proveedor) values (%s,%s)', (request.form['nombre_proveedor'], request.form['rut_proveedor']))
        mysql.connection.commit()
        sll = cur.execute('select * FROM factura')
        id_factura = sll  
        cur.execute('insert into detalle_factura (id_factura, identificador_producto, nombre_producto, fecha_factura, cantidad) values (%s,%s,%s,%s,%s)', (id_factura, request.form['codigo_producto'], request.form['nombre_producto'], request.form['fecha_factura'], request.form['cantidad']))
        mysql.connection.commit()
        if(int(request.form['cantidad']) >= 1):
            for i in range(int(request.form['cantidad'])):
                cur.execute('insert into registro_componente (id_detalle_factura, nombre_producto) values (%s,%s)', (id_factura, request.form['nombre_producto']))
                mysql.connection.commit()
                cur.execute('insert into detalle_registro_componente (id_registro_Componente) values ('"%s"')', (id_factura, ))
                mysql.connection.commit() 
        cur.close()

        return render_template('index.html')

@app.route('/form_pic',methods = ['POST'])
def form_pic():
    if(request.method == 'POST'):
        id_usuario = request.form['id_usuario']
        fecha = date.today()
        tipo_producto = "pic"
        estado_disponibilidad = 0
        #usuario
        cur = mysql.connection.cursor()
        user = cur.execute('SELECT * FROM usuario')
        #
        cur.execute('insert into detalle_registro_componente (id_registro_Componente) values ('"%s"')', (id_factura, ))
        mysql.connection.commit() 
        cur.close()
        if(int(id_usuario) <= int(user) and int(id_usuario) >= 0):
            id_usuario = request.form['id_usuario']
        else:
            print("here")
            return render_template('usuario_no_encontrado.html')



if __name__ == "__main__":
    app.run(port=3000 ,debug=True)































































