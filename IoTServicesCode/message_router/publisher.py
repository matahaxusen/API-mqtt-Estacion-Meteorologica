import time
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print ('EXITO en la conexion')
    else:
        print ('ERROR de conexion con codigo :', {rc})


client = mqtt.Client()


def make_connection():
    client.username_pw_set(username='g100363709', password='Jorge.97')
    client.on_connect = on_connect
    client.connect('35.242.198.119', 1883, 60)
    print ('conexion con exito')


def send_temperature(temperatura):
    print ('temperatura publicada', temperatura)
    client.publish('temperature', payload=temperatura, qos=0, retain=False)
    time.sleep(1)


def send_humidity(humedad):
    print ('humedad publicada', humedad)
    client.publish('humidity', payload=humedad, qos=0, retain=False)
    time.sleep(1)


def send_id(device_id):
    print ('Dispositivo publicado', device_id)
    client.publish('devices', payload=device_id, qos=0, retain=False)
    time.sleep(1)

def send_ubication(ubicacion):
    print ('Ubicacion publicada', ubicacion)
    client.publish('ubication', payload=ubicacion, qos=0, retain=False)
    time.sleep(1)


def send_date(fecha):
    print ('Fecha registrada', fecha)
    client.publish('date', payload=fecha, qos=0, retain=False)
    time.sleep(1)


def send_bye(fecha):
    print ('Usuario desconectado: ', fecha)
    client.publish('bye', payload=fecha, qos=0, retain=False)
    time.sleep(1)
