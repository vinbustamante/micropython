from machine import ADC
import time
import machine

adc = ADC(0)

while True:
    lightIntensity = adc.read()
    print('read : ', lightIntensity)
    time.sleep(1)

