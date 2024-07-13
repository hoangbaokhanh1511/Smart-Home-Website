import dht, ujson, uasyncio as asyncio, urequests
import machine
from machine import I2C, Pin

from esp8266_i2c_lcd import I2cLcd
from OOP import *

# Khai Báo Đèn
led = {
    "Led_Main": LED(pin_number=2),
    "Led_D7": LED(pin_number=13),
    "Led_D8": LED(pin_number=15)
}
url_host = 'http://192.168.1.7:5000'
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
    url = url_host + '/user_dashboard/api/weather'
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
    url = url_host + '/user_dashboard/api/motion'
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
    url = url_host + '/user_dashboard/api/change_status_led'
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
#

async def LCD():

    DEFAULT_I2C_ADDR = 0x27
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    lcd.putstr("Bai thuc hanh 5 \nGiao tiep LCD")

async def main():
    await LCD()
    await asyncio.gather(

        send_dht11(),
        send_pir(),
        toggleLed()
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
