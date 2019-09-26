import onewire, ds18x20, machine
import time


data = machine.Pin(14)
ds = ds18x20.DS18X20(onewire.OneWire(data))
roms = ds.scan()
print('roms : ', roms)
ds.convert_temp()    
time.sleep_ms(750)
print('temp : ', ds.read_temp(roms[0]))

# while True:
#     ds.convert_temp()    
#     print('temp : ', ds.read_temp(roms[0]))
#     time.sleep(2)
   