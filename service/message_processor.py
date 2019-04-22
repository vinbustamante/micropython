from lib.pin import Led

led = Led(5)
def message_receive(topic, payload):    
    if payload == b'1':
        led.on()
    else:
        led.off()