import dht, ujson, uasyncio as asyncio, urequests
from machine import I2C
from module.esp8266_i2c_lcd import I2cLcd
from OOP import *
from module.MQ135 import MQ135


# Khai Báo Đèn Bật Tắt và điều chỉnh độ sáng của đèn
led = {
    "Led_Main": LED(pin_number=2),
    "Led_D7": LED(pin_number=13),
    "Led_D8": LED(pin_number=15)
}

url_host = 'http://192.168.1.5:5000'

# Pir sensor pir HC-SR501
pir = motion_detect(pin_number=14)

# sensor DHT11
sensor = sensor_dht11(pin_number=16)

# MQT135
adc = MQ135(0)


def weather():
    temperature, humidity = sensor.get_weather()
    data = {
        'temperature': temperature,
        'humidity': humidity
    }
    return data


async def send_pir():
    url = url_host + '/api/motion'
    while True:
        data = {'Bathroom': True if pir.get_status() else False, 'Area2': False}
        headers = {'Content-Type': 'application/json'}

        led['Led_Main'].toggle(0) if data['Bathroom'] == True else led['Led_Main'].toggle(1023)
        try:
            response = urequests.post(url, data=ujson.dumps(data), headers=headers)

            response.close()
        except OSError as e:
            print('Error loading LED:', e)

        await asyncio.sleep(5)


async def toggleLed():
    url = url_host + '/api/change_status_led'
    while True:
        response = urequests.get(url)
        data = response.json()

        led['Led_Main'].toggle(data['Led_Main'])
        led['Led_D7'].toggle(data['Led_D7'])
        led['Led_D8'].toggle(data['Led_D8'])

        response.close()
        await asyncio.sleep(0.1)


async def MQT135():
    url = url_host + '/api/mqt135'
    while True:
        data = weather()
        value = adc.get_corrected_ppm(data['temperature'], data['humidity'])
        print(value)
        mqt = {
            'value': value
        }
        response = urequests.post(url=url, headers={'Content-Type': 'application/json'}, data=ujson.dumps(mqt))
        response.close()
        await asyncio.sleep(3)


async def LCD():
    data = weather()
    DEFAULT_I2C_ADDR = 0x27
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    celcius = bytearray([
        0x0E,
        0x11,
        0x11,
        0x0E,
        0x00,
        0x00,
        0x00,
        0x00
    ])
    lcd.custom_char(0, celcius)
    lcd.putstr(f"Nhiet Do: {data.get('temperature')}")
    lcd.putchar(chr(0))
    lcd.putstr(f"C\nDo am: {data.get('humidity')}%")
    await asyncio.sleep(2)


async def dht11():
    url = url_host + '/api/weather'
    while True:
        data = weather()
        up_data = {
            'temperature': data.get('temperature'),
            'humidity': data.get('humidity')
        }
        response = urequests.post(data=ujson.dumps(up_data), headers={"Content-Type": "application/json"}, url=url)
        response.close()
        await asyncio.sleep(5)


async def main():
    await asyncio.gather(
        MQT135(),
        dht11(),
        # LCD(),
        send_pir(),
        toggleLed(),
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
