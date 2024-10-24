from machine import Pin,PWM
from time import sleep
import dht

class LED:
    def __init__(self, pin_number):
        self.led = Pin(pin_number, Pin.OUT)
    def On(self):
        return self.led.value(1)
    def Off(self):
        return self.led.value(0)

class Fan:
    def __init__(self, pin_number):
        self.fan = Pin(pin_number, Pin.OUT)
    def On(self):
        return self.fan.value(1)
    def Off(self):
        return self.fan.value(0)

class sensor_dht11:
    def __init__(self, pin_number):
        self.sensor = dht.DHT11(Pin(pin_number))
        self.sensor.measure()

    def get_weather(self):
        return self.sensor.temperature(), self.sensor.humidity()


class motion_detect:
    def __init__(self, pin_number):
        self.pir = Pin(pin_number, Pin.IN)
        self.pir.value(0)
    def get_status(self):
        return self.pir.value()
