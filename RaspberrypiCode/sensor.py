import signal
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
import re,uuid
import lcd
from datetime import datetime
from IoTServicesCode.message_router.publisher import *
from IoTServicesCode.microservices.measurements_microservices import gps

# configuramos la motherboard
GPIO.setmode(GPIO.BCM)
# configuramos el boton
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def signal_handler(sig, frame):
    make_connection()
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    send_bye(mac)
    GPIO.cleanup()
    sys.exit(0)


def button_callback(channel):
    global DISPLAY_MODE
    print ('modificando display...')
    if DISPLAY_MODE < 1:
        DISPLAY_MODE += 1
    else:
        DISPLAY_MODE = -1


def when_am_i():
    date = datetime.now()
    now = str(date.day)+'/'+str(date.month)+'/'+str(date.year)+' '+str(date.hour)+':'+str(date.minute)+':'+str(date.second)
    return now


def lcd_printer(temp, hum):
    global DISPLAY_MODE
    if DISPLAY_MODE == -1:
        lcd.lcd_message('Temp.*C: ' + str(temp), 'Humedad: ' + str(hum) + '%')
    if DISPLAY_MODE == 0:
        lcd.lcd_message('Temperatura:',str(temp) + '*C')
    if DISPLAY_MODE == 1:
        lcd.lcd_message('Humedad:',str(hum) + '%')

def weatherSensor():
    # configuramos el sensor con nuestro tipo (puede ser DHT11 o DHT12)
    DHT_SENSOR = Adafruit_DHT.DHT11
    # configuracion de los componentes
    DHT_GPIO = 4

    nueva_temperatura = -1.0
    nueva_humedad = -1.0
    nueva_ubicacion = '0,0'
    nueva_fecha = datetime(2021, 1, 1, 00, 00, 00, 00001)

    while True:
        humedad, temperatura = Adafruit_DHT.read(DHT_SENSOR, DHT_GPIO)
        ubicacion = gps.gps_ll('Avenida Betanzos 83 Madrid')
        fecha = datetime.now()

        if humedad is not None and temperatura is not None and humedad < 101 and humedad > 1:
            global DISPLAY_MODE
            if (nueva_temperatura != temperatura):
                nueva_temperatura = temperatura
                nueva_fecha = fecha
                send_temperature(temperatura)
                time.sleep(0.5)
            if (nueva_humedad != humedad):
                nueva_humedad = humedad
                nueva_fecha = fecha
                send_humidity(humedad)
                time.sleep(0.5)
            print ('Temperatura: {0:0.1f}C Humedad: {1:0.1f}%'.format(temperatura,humedad))
            if fecha.minute != nueva_fecha.minute:
                nueva_fecha = fecha
                send_date(when_am_i())
                time.sleep(0.5)
            if nueva_ubicacion != ubicacion:
                nueva_ubicacion = ubicacion
                nueva_fecha = fecha
                send_ubication(ubicacion)
                time.sleep(0.5)
            lcd_printer(temperatura, humedad)
            time.sleep(5)
        else:
            lcd.lcd_message('ERROR de lectura', 'del sensor')
            print ('Fallo en la lectura del sensor')
            time.sleep(5)



if __name__ == "__main__":
    make_connection()
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    send_date(when_am_i())
    send_ubication(gps.gps_ll('Avenida Betanzos 83 Madrid'))
    send_id(mac)
    GPIO.add_event_detect(16, GPIO.RISING, callback=button_callback, bouncetime=300)
    signal.signal(signal.SIGINT, signal_handler)
    DISPLAY_MODE = 0
    weatherSensor()
