from machine import Pin,PWM
from time import sleep
import dht

class LED:
    def __init__(self, pin_number):
        self.led = Pin(pin_number, Pin.OUT)
        self.pwm = PWM(self.led, freq=10000)
        self.brightness = 0


    def toggle(self, value):

        if value == 0 or value == 1023:
            self.brightness = value
            self.pwm.duty(self.brightness)

        else:

            if self.brightness < value:
                for duty in range (self.brightness,value,25):
                    self.pwm.duty(duty)
                    sleep(0.01)
            else:
                for duty in range (self.brightness,value,-25):
                    self.pwm.duty(duty)
                    sleep(0.01)

            self.brightness = value


        return self


class sensor_dht11:
    def __init__(self, pin_number):
        self.sensor = dht.DHT11(Pin(pin_number))
        self.sensor.measure()

    def get_weather(self):
        return self.sensor.temperature(), self.sensor.humidity()


class motion_detect:
    def __init__(self, pin_number):
        self.pir = Pin(pin_number, Pin.IN)

    def get_status(self):
        return self.pir.value()
