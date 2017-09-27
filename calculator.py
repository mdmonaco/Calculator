from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import g
from contextlib import closing
import math
import sqlite3


app = Flask(__name__)

list_input = []
list_output = []



DATABASE = './data/database.db'

# Funcion connect_db
# Descripcion: Instancia la conexion de la base de datos
# Parametros: DB
# Respuesta: Conexion con la base de datos

def connect_db():
    return sqlite3.connect(DATABASE)

# Funcion before_request
# Descripcion: Abre la base de datos cuando recibe una solicitud de la misma
# Parametros: DB
# Respuesta: Conexion con la base de datos establecida

@app.before_request
def before_request():
    g.db = connect_db()

# Funcion after_request
# Descripcion: Cierra la base de datos luego de la solicitud
# Parametros: DB
# Respuesta: Conexion con la base de datos cerrada

@app.after_request
def after_request(response):
    g.db.close()
    return response

# Funcion init_db
# Descripcion: Inicializa la base de datos asignandole un esquema
# Parametros: DB
# Respuesta: Base de datos con el schema asignado


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('./data/schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Funcion insert
# Descripcion: Genera el query de la insercion de datos en una tabla determinada y lo ejecuta
# Parametros: String(tabla)
# Parametros: Tupla(Campos)
# Parametros: Tupla(Valores)
# Respuesta: Devuelve el id de la ultima linea de datos insertada

def insert(table, fields=(), values=()):
    # g.db is the database connection
    cur = g.db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.db.commit()
    id = cur.lastrowid
    cur.close()
    return id

# Funcion insert
# Descripcion: Genera el query de la consulta de los datos de una sesion particular y lo ejecuta
# Parametros: String(session)
# Respuesta: Devuelve un registro con todos los datos de una sesion particular

def select(session):
    # g.db is the database connection
    list_input = []
    cur = g.db.execute("SELECT * FROM calculos WHERE session='%s'" % session)
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

# Funcion: log
# Descripcion: Hace el calculo de la funcion logaritmo
# Parametros: Int(dato1)
# Parametros: Int(dato2)
# Respuesta: Devuelve el resultado de log(dato1,dato2) 

def log(a,b):
    return math.log(a,b)

# Api metodo GET route /
# Descripcion: Renderiza el index.html
# Parametros: String(Nombre del html)
# Respuesta: Muestra en http://localhost:5000 el html renderizado  

@app.route('/')
def vista():
    return render_template('index.html')

# Api metodo GET route /save
# Descripcion: Guarda los datos almacenados temporalmente en una sesion especifica
# Parametros: String(session)
# Respuesta: Resultado del guardado de los datos en la base de datos

@app.route('/save')
def	save():
    if request.args.get('a'," ",type=str)=="":
        return jsonify("Debe ingresar el nombre de la session para poder guardar")
    session = request.args.get('a'," ",type=str).lower()
    if len(list_input)==0 :
        return jsonify("No tiene datos para guardar")
    for i in range(len(list_output)):  #Guarda todos los inputs y outpus en la base
	   insert('calculos', ('session','input','output'), (session,list_input[i],list_output[i]))
    del list_output[:]
    del list_input[:]
    return jsonify('save')

# Api metodo GET route /show
# Descripcion: Genera un registro de datos guardados de una session particular
# Parametros: String(session)
# Respuesta: Un registro con los datos extraidos de la base de una sesion particular

@app.route('/show')
def show():
    if request.args.get('a'," ",type=str)=="":
        return jsonify("Debe ingresar el nombre de la session para poder recuperar una sesion")
    return select(request.args.get('a'," ",type=str).lower())

# Api metodo GET route /calcular
# Descripcion: Realiza los calculos de una formula matematica
# Parametros: String(input)
# Respuesta: Un string con el resultado del calculo de la formula, de ser correcta. Caso contrario retorna error

@app.route('/calcular/')
def calcular():
    calculo = request.args.get('a',0,type=str)
    if calculo== '':
        return jsonify('Error1')
    try:
        resul_calculo = eval(calculo) 
    except Exception as e:
        return jsonify('Error2')
    else:
        list_input.append(calculo)    #Agrega el input a una lista
        list_output.append(resul_calculo)   #Agrega el output a una lista
        return jsonify(resul_calculo)




if __name__ == '__main__':
    app.run()