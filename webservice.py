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





DATABASE = './database/database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('./database/schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

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

def inputs(lista,elem):
    return lista.append(elem) 

@app.route('/')
def vista():
    return render_template('index.html')

def log(a,b):
	return math.log(a,b)

@app.route('/save')
def	save():
    for i in range(len(list_input)):  #Guarda todos los inputs y outpus en la base
	   insert('calculos', ('input','output'), (list_input[i],list_output[i]))
    return jsonify("Se han guardado los datos")

@app.route('/show')
def show():
    return jsonify("mostrar datos")

@app.route('/calcular/')
def calcular():
    calculo = request.args.get('a',0,type=str)
    if calculo== '':
        return jsonify(0)
	#insert('calculos', ('input','output'), (calculo,eval(calculo))
	#return jsonify(eval(caculo))
    list_input.append(calculo)    #Agrega el input a una lista
    list_output.append(eval(calculo))   #Agrega el output a una lista
    return jsonify(eval(calculo))



if __name__ == '__main__':
    app.run()