import dht, ujson, uasyncio as asyncio, urequests
from time import sleep
from machine import I2C, Pin, PWM
from esp8266_i2c_lcd import I2cLcd
from OOP import *

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


# API thời tiết local
# API_key = "07bb5510d2576951d78b0f0b637f4716"
# ion = 107.5796
# iat = 16.4637
# data = (urequests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={iat}&lon={ion}&appid={API_key}")).json()


def weather():
    temperature, humidity = sensor.get_weather()

    data = {
        'temperature': temperature,
        'humidity': humidity
    }

    return data


async def API_weather():
    url = url_host + '/user_dashboard/api/weather'

    while True:
        API_key = "993e2f3c8044ed3f8a149993504ae427"
        CITY = "Hue"
        data = urequests.get(f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_key}").json()

        up_data = {
            'temperature': data['main']['temp'] - 273,
            'humidity': data['main']['humidity'],
            'feels_like': data['main']['feels_like'] - 273,
            'main': data['weather'][0]['main'],
            'visibility': data['visibility']
        }

        respone = urequests.post(url, data=ujson.dumps(up_data), headers={'Content-type': 'application/json'})
        respone.close()

        await asyncio.sleep(900)


async def send_pir():
    url = url_host + '/user_dashboard/api/motion'
    while True:
        data = {'status': True if pir.get_status() else False}
        headers = {'Content-Type': 'application/json'}
        try:
            response = urequests.post(url, data=ujson.dumps(data), headers=headers)

            response.close()
        except OSError as e:
            print('Error loading LED:', e)

        await asyncio.sleep(10)


async def toggleLed():
    url = url_host + '/user_dashboard/api/change_status_led'
    while True:
        response = urequests.get(url)
        data = response.json()


        led['Led_Main'].toggle(data['Led_Main'])
        led['Led_D7'].toggle(data['Led_D7'])
        led['Led_D8'].toggle(data['Led_D8'])


        response.close()
        await asyncio.sleep(0.3)


# adc = ADC(0)
# async def MQT135():
#
#     while True:
#         adc_value = adc.read()
#         co2_concentration = adc_value * 2.5
#         nh3_concentration = adc_value * 1.8
#         co_concentration = adc_value * 1.3
#         ethanol_concentration = adc_value * 1.5
#
#         print(f"Nồng độ co2 {co2_concentration} đơn vị ppm")
#         print(f"Nồng độ nh3 {nh3_concentration} đơn vị ppm")
#         print(f"Nồng độ co {co_concentration} đơn vị ppm")
#         print(f"Nồng độ ethanol {ethanol_concentration} đơn vị ppm")
#         await asyncio.sleep(1)


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



async def main():
    await asyncio.gather(
        LCD(),
        API_weather(),
        send_pir(),
        toggleLed(),
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
