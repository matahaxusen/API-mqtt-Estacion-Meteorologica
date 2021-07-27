import json
import paho.mqtt.client
import requests
from load_env import load_env

my_json = []
with open('weather.json', 'w') as json_file:
    json_file.write('')


def insert_measures(temp, hum, ubication, date, dev):
    json = {'temperature': temp, 'humidity': hum, 'ubication': ubication, 'date': date,'device_id': dev}
    requests.post('http://' + env['micro-ip'] + ':5000/insert_measures', data=json)


def insert_device(dev, ubication, date):
    json = {'device_id': dev,'ubication':ubication,'date':date}
    requests.post('http://' + env['micro-ip'] + ':5000/insert_device', data=json)

def good_bye(dev, ubication, date):
    json = {'device_id': dev,'ubication':ubication,'date':date}
    requests.post('http://' + env['micro-ip'] + ':5000/good_bye', data=json)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print ('Connect success')
        client.subscribe('humidity')
        client.subscribe('temperature')
        client.subscribe('devices')
        client.subscribe('ubication')
        client.subscribe('date')
        client.subscribe('bye')
    else:
        print ('Connect failure, code: ', rc)


def on_message(client, userdata, msg):
    global temp, hum, ubication, date, dev
    print ({msg.topic}, {msg.payload})
    if msg.topic == 'temperature':
        temp = float(msg.payload.decode('utf-8'))
        insert_measures(temp, hum, ubication, date, dev)
        print (temp, hum, ubication, date)
        dict = {'temperature': temp, 'humidity': hum, 'ubication': ubication, 'date': date}
        with open('weather.json', 'a') as json_file:
            json_str = json.dumps(dict, indent=0)
            json_file.write(json_str)
            json_file.write('\n')
    if msg.topic == 'humidity':
        hum = float(msg.payload.decode('utf-8'))
        insert_measures(temp, hum, ubication, date, dev)
        print (temp, hum, ubication, date)
        dict = {'temperature': temp, 'humidity': hum, 'ubication': ubication, 'date': date}
        with open('weather.json', 'a') as json_file:
            json_str = json.dumps(dict, indent=0)
            json_file.write(json_str)
            json_file.write('\n')
    if msg.topic == 'ubication':
        ubication = str(msg.payload.decode('utf-8'))
        insert_measures(temp, hum, ubication, date, dev)
        print (temp, hum, ubication, date)
        dict = {'temperature': temp, 'humidity': hum, 'ubication': ubication, 'date': date}
        with open('weather.json', 'a') as json_file:
            json_str = json.dumps(dict, indent=0)
            json_file.write(json_str)
            json_file.write('\n')
    if msg.topic == 'date':
        date = str(msg.payload.decode('utf-8'))
        insert_measures(temp, hum, ubication, date, dev)
        print (temp, hum, ubication, date)
        dict = {'temperature': temp, 'humidity': hum, 'ubication': ubication, 'date': date}
        with open('weather.json', 'a') as json_file:
            json_str = json.dumps(dict, indent=0)
            json_file.write(json_str)
            json_file.write('\n')
    if msg.topic == 'bye':
        dev = str(msg.payload.decode('utf-8'))
        good_bye(dev,ubication,date)
        print (dev)
    elif msg.topic == 'devices':
        dev = str(msg.payload.decode('utf-8'))
        insert_device(dev,ubication,date)
        print (dev)

temp = 0
hum = 0
ubication = '0,0'
date = '01/01/2021 00:00:01'
env = load_env()
dev = '**:**:**:**:**:**'
mqtt = paho.mqtt.client.Client()
mqtt.username_pw_set(username=env['mqtt-user'], password=env['mqtt-pswd'])
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect(env['mqtt-ip'], 1883, 60)
mqtt.loop_forever()
