from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
import mysql.connector
from load_env import load_env

envy = load_env()
db = mysql.connector.connect(host=envy['mariadb-ip'], user=envy['mariadb-user'], password=envy['mariadb-pswd'],
                             database=envy['mariadb-db'])
app = Flask(__name__)
CORS(app)


def no_insert_default(data):
    if data['humidity'] == 0 or data['ubication'] == '0,0' or data['date'] == '01/01/2021 00:00:01' or data['temperature'] == 0 or data['device_id'] == '**:**:**:**:**:**':
        return False
    else:
        return True


@app.route('/insert_device', methods=['POST'])
def insert_device():
    data = request.form
    sql = 'INSERT INTO devices (device_id,status,ubication,last_reg) VALUES (%s,%s,%s,%s)'
    val = (data['device_id'], 'activo', data['ubication'], data['date'])
    print (sql, val)
    try:
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print (mycursor.rowcount, 'records inserted')
        return 'ok'
    except:
        sql = 'UPDATE devices SET device_id=%s,status=%s,last_reg=%s,ubication=%s WHERE device_id=%s'
        val = (data['device_id'], 'activo', data['date'], data['ubication'], data['device_id'])
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        return 'ok'


@app.route('/good_bye', methods=['POST'])
def good_bye():
    data = request.form
    sql = 'UPDATE devices SET device_id=%s,status=%s,last_reg=%s,ubication=%s WHERE device_id=%s'
    val = (data['device_id'], 'inactivo', data['date'], data['ubication'], data['device_id'])
    mycursor = db.cursor()
    mycursor.execute(sql, val)
    db.commit()
    return 'ok'


@app.route('/insert_measures', methods=['POST'])
def insert_measures():
    data = request.form
    if no_insert_default(data):
        sql = 'INSERT INTO sensor_data (temperature,humidity,ubication,reg_date,device_id) VALUES (%s,%s,%s,%s,%s)'
        val = (data['temperature'], data['humidity'], data['ubication'], data['date'], data['device_id'])
        print (sql, val)
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print (mycursor.rowcount, 'records inserted')
        return 'ok'
    else:
        print ('Reconocido un valor por defecto, cancelando la insercion')
        return 'out'


@app.route('/sensor_list')
def sensor_list():
    muestreo = {}
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 6')
        sql_dict = cursor.fetchall()
        db.commit()
        muestreo = sql_dict
    return jsonify(muestreo)


@app.route('/devices_list')
def devices_list():
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM devices ORDER BY id ASC')
        sql_dict = cursor.fetchall()
        db.commit()
        muestreo = sql_dict
    return jsonify(muestreo)


@app.route('/busqueda')
def busqueda():
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM sensor_data')
        sql_dict = cursor.fetchall()
        db.commit()
    return jsonify(sql_dict)


@app.route('/hello_world')
def hello_world():
    return {'msg':'hello world'}


app.run(host='0.0.0.0', port=5000)
