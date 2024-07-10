import dht, ujson, uasyncio as asyncio, urequests
from OOP import *

# Khai Báo Đèn
led = {
    "Led_Main": LED(pin_number=2),
    "Led_D7": LED(pin_number=13),
    "Led_D8": LED(pin_number=15)
}
url_host = 'http://192.168.1.3:5000'
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


async def send_dht11():
    url = url_host + '/api/weather'
    while True:
        data = weather()

        headers = {'Content-Type': 'application/json'}
        try:
            response = urequests.post(url, data=ujson.dumps(data), headers=headers)
            response.close()
        except OSError as e:
            print('Error loading LED:', e)

        await asyncio.sleep(5)


async def send_pir():
    url = url_host + '/api/motion'
    while True:
        data = {'status': True if pir.get_status() else False}
        headers = {'Content-Type': 'application/json'}
        try:
            response = urequests.post(url, data=ujson.dumps(data), headers=headers)

            response.close()
        except OSError as e:
            print('Error loading LED:', e)

        await asyncio.sleep(3)


async def toggleLed():
    url = url_host + '/api/change_status_led'
    while True:
        response = urequests.get(url)
        data = response.json()

        if data['Led_Main']:
            led.get('Led_Main').turn_off()
        else:
            led.get('Led_Main').turn_on()

        if data['Led_D7']:
            led.get('Led_D7').turn_on()
        else:
            led.get('Led_D7').turn_off()

        if data['Led_D8']:
            led.get('Led_D8').turn_on()
        else:
            led.get('Led_D8').turn_off()

        response.close()
        await asyncio.sleep(0.2)


async def main():
    await asyncio.gather(
        send_dht11(),
        send_pir(),
        toggleLed()
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
