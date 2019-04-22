import machine
import time
import lib.util as util

# init
led = machine.Pin(5, machine.Pin.OUT)
button = machine.Pin(0, machine.Pin.IN)

while True:
    status = button.value()
    if not status:
        print('flash led')
        util.flash_led(led)
    else:
        led.off()
    time.sleep(0.1)