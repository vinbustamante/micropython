from machine import Pin
import utime as time

class Led:

    def __init__(self, pinNumber):
        self._led = Pin(pinNumber, Pin.OUT)
        self._isOn = 0
        self._led.off()

    def on(self):
        self._isOn = 1
        self._led.on()

    def off(self):
        self._isOn = 0
        self._led.off()

    def toggle(self):
        if self._isOn:
            self.off()
        else:
            self.on()

class Button:

    def __init__(self, pinNumber):
        self._button = Pin(pinNumber, Pin.IN)

    def isPress(self):
        value = self._button.value()
        if value:
            return 1
        else:
            return 0