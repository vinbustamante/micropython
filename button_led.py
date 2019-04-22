import machine
import utime as time

button = machine.Pin(4, machine.Pin.IN)
led = machine.Pin(5 , machine.Pin.OUT)
led.off()
while True:
    value = button.value()
    if value:
        print('on')
        led.on()
    else:
        led.off()