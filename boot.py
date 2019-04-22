# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc #active
#import webrepl
#webrepl.start()
gc.collect() # active