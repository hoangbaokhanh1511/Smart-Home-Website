from machine import Pin
from time import sleep
import dht, ujson, gc
import usocket as socket
from OOP import *

# Khai Báo Đèn
led = {
    "Led_Main": LED(pin_number=2),
    "Led_First": LED(pin_number=13),
    "Led_Second": LED(pin_number=15)
}

# Pir sensor pir HC-SR501
pir = motion_detect(pin_number=14)

# sensor DHT11
sensor = sensor_dht11(pin_number=16)


def weather():
    temperature, humidity = sensor.get_weather()

    data = {
        'temperature': temperature,
        'humidity': humidity
    }

    return data


def web_page():
    with open('templates/index.html', 'r', encoding='utf-8') as file:
        html = file.read()
    return html


def handle_request(request):
    if 'GET /led' in request:
        value = ''

        if "led=off" in request:
            led['Led_Main'].turn_on()
            value = 'on'


        elif "led=on" in request:
            led['Led_Main'].turn_off()
            value = 'off'


        elif "led1=on" in request:
            led['Led_First'].turn_on()
            value = 'on'

        elif "led1=off" in request:
            led['Led_First'].turn_off()
            value = 'off'


        elif "led2=on" in request:
            led['Led_Second'].turn_on()
            value = 'on'


        elif "led2=off" in request:
            led['Led_Second'].turn_off()
            value = 'on'

        response = {
            'state': str(value)
        }

        return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + ujson.dumps(response)

    elif 'GET /api/weather' in request:
        response = weather()

        return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + ujson.dumps(response)

    elif 'GET /api/motion' in request:
        response = {'status': True if pir.get_status() else False}
        if pir.get_status():
            led['Led_Main'].turn_off()
        else:
            led['Led_Main'].turn_on()
        return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + ujson.dumps(response)



    elif 'GET /' in request:

        response = web_page()

        return 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response

    else:
        return 'HTTP/1.1 404 NOT FOUND\r\n\r\n', None


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()

        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Content = %s' % request)

        response = handle_request(request)

        conn.sendall(response)
        conn.close()

    except OSError as e:
        conn.close()
