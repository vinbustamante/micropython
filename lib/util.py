import time
import ujson as json

def flash_led(signal):
    for i in range(0, 25):
        signal.on()
        time.sleep(0.001)
        signal.off()
        time.sleep(0.001)

def stringToBytes(str):
    values = bytearray()
    values.extend(str)
    return values

def bytesToString(value):
    return value.decode("utf-8")

def toJson(value):
        return json.dumps(value)