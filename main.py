import ujson, uasyncio as asyncio, urequests
from OOP import *
from machine import I2C, ADC
from esp8266_i2c_lcd import I2cLcd

url_host = 'http://172.20.10.9:5000'

# Khai Báo Đèn Bật Tắt của đèn
light = LED(pin_number=12)

# Pir sensor pir HC-SR501
pir = motion_detect(pin_number=14)
led = Pin(15,Pin.OUT)
#Quạt
fan1 = Fan(pin_number=0)
fan2 = Fan(pin_number=13)

# sensor DHT11
sensor = sensor_dht11(pin_number=16)

# MQT2
adc = ADC(0)

def weather():
    temperature, humidity = sensor.get_weather()
    data = {
        'temperature': temperature,
        'humidity': humidity
    }
    return data

async def mqt2():
    while True:
        url = url_host + '/api/mqt2'
        value = adc.read()
        data = {"value": value}
        headers = {"Content-Type": "application/json"}
        try:
            response = urequests.put(url, data=ujson.dumps(data), headers=headers)
            response.close()
        except OSError as e:
            print("Error loading MQT2: ", e)

        await asyncio.sleep(3)


async def send_pir():
    url = url_host + '/api/motion'
    while True:
        data = {'status': True if pir.get_status() else False}
        headers = {'Content-Type': 'application/json'}
        print(pir.get_status())
        led.on() if pir.get_status() else led.off()
        try:
            response = urequests.put(url, data=ujson.dumps(data), headers=headers)
            response.close()
        except OSError as e:
            print('Error loading LED:', e)

        await asyncio.sleep(5)


async def toggleLed():
    url = url_host + '/api/light'
    while True:
        response = urequests.get(url)
        data = response.json()

        light.On() if data.get('status') else light.Off()

        response.close()
        await asyncio.sleep(0.4)

async def toggleFan():
    url = url_host + '/api/fan'
    while True:
        response = urequests.get(url)
        data = response.json()

        f1 = data.get('fan1')
        f2 = data.get('fan2')

        fan1.On() if f1 else fan1.Off()
        fan2.On() if f2 else fan2.Off()

        response.close()
        await asyncio.sleep(0.5)


async def dht11():
    url = url_host + '/api/dht11'
    while True:
        data = weather()
        up_data = {
            'temperature': data.get('temperature'),
            'humidity': data.get('humidity')
        }
        response = urequests.put(data=ujson.dumps(up_data), headers={"Content-Type": "application/json"}, url=url)
        response.close()
        await asyncio.sleep(10)

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
    await asyncio.sleep(10)

async def main():
    await asyncio.gather(
        send_pir(),
        toggleLed(),
        toggleFan(),
        LCD(),
        dht11(),
        mqt2()
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
