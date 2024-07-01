import time
from machine import Pin
from time import sleep
import dht, ujson, urequests

# Khai Báo Đèn
led = Pin(2, Pin.OUT, value=1)
led1 = Pin(13, Pin.OUT, value=0)
led2 = Pin(15, Pin.OUT, value=0)

# Gọi API thời tiết
API_KEY = '07bb5510d2576951d78b0f0b637f4716'
LAT = 16.467
LON = 107.590
URL = f'http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'

def get_weather():
    try:
        response = urequests.get(URL)
        data = response.json()

        required = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity']
        }

        return required
    except Exception as e:
        return e

# Pir sensor pir HC-SR501
pir = Pin(14, Pin.IN)


def web_page():
    with open('templates/index.html', 'r', encoding='utf-8') as file:
        html = file.read()
    return html


def handle_request(request):
    if 'GET /led' in request:
        value = ''

        if "led=on" in request:
            led.off()
            value = 'on'


        elif "led=off" in request:
            led.on()
            value = 'off'


        elif "led1=on" in request:
            led1.on()
            value = 'on'

        elif "led1=off" in request:
            led1.off()
            value = 'off'


        elif "led2=on" in request:
            led2.on()


        elif "led2=off" in request:
            led2.off()

        response = {
            'state': str(value)
        }

        return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + ujson.dumps(response)

    elif 'GET /api/weather' in request:
        response = get_weather()
        return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + ujson.dumps(response)

    elif 'GET /api/motion' in request:
        response = {'status' : True if pir.value() else False}
        return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + ujson.dumps(response)

    elif 'GET /' in request:
        response = web_page()
        return 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response


    else:
        return 'HTTP/1.1 404 NOT FOUND\r\n\r\n'


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
