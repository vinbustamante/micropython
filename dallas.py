import onewire, ds18x20, machine
#from lib.pin import Led
import time
# from service.setting import Setting
# import service.network as networkService

#led = Led(2)
data = machine.Pin(12)
ds = ds18x20.DS18X20(onewire.OneWire(data))
roms = ds.scan()
print('test :', roms)
#print('temp : ', ds.read_temp(roms[0]))

while True:
    ds.convert_temp()
    time.sleep(1)
    print('temp : ', ds.read_temp(roms[0]))
    time.sleep(1)
    #led.off()
    #time.sleep(1)
    #led.on()