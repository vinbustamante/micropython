import time
import machine
from machine import ADC
adc = ADC(0)

while True:
    time.sleep(1)
    lightIntensity = adc.read()
    print(lightIntensity)