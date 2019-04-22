import time
from lib.pin import Led

led = Led(5)
while True:
    led.toggle()
    time.sleep(0.5)