import machine
import time

led = machine.Pin(5, machine.Pin.OUT)
led.on()

while True:
    print('off')
    led.on()
    time.sleep(0.5)
    print('on')
    led.off()
    time.sleep(0.5)