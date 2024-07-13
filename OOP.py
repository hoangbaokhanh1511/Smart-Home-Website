from machine import Pin
import dht


class LED:
    GPIO = -1
    def __init__(self, pin_number):
        self.led = Pin(pin_number, Pin.OUT)
        self.led.value(0)
        self.GPIO = pin_number

    def turn_on(self):
        self.led.on()

    def turn_off(self):
        self.led.off()

    def __str__(self):
        return f"This is GPIO {self.GPIO}"


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
