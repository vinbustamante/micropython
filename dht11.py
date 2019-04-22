import machine
import time
import dht

dht11 = dht.DHT11(machine.Pin(14))

while True:
    time.sleep(1)
    dht11.measure()
    print('temp : ', dht11.temperature())
    print('hum : ', dht11.humidity())