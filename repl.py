import machine
import time
from lib.wlan import Wifi
from lib.umqttsimple import MQTTClient
from lib.pin import Led
import socket
import network

led = Led(2)

wifi = Wifi('Redbean_24GHZ','homeboys')
wifi.connect()
while not wifi.is_connected():
    machine.idle()
    time.sleep(1)    
print('wifi connected')
print(wifi._wlan.config('dhcp_hostname'))

def message_receive(topic, payload):
    print(topic, payload)
    if payload == b'1':
        print('light on')
        led.on()
    else:
        print('light off')
        led.off()

def run(server):
    c = MQTTClient("umqtt_client", server, ssl_params={"ca_certs":"cert/ca.crt", "certfile": "cert/device001.crt", "keyfile": "cert/device001.key"})
    c.set_callback(message_receive)
    c.connect()
    print('Connected now')
    # c.subscribe(b"home/livingroom/temperature")
    # while True:
    #     # if True:
    #         # Blocking wait for message
    #     #c.wait_msg()
    #     # else:
    #     #     # Non-blocking wait for message
    #     #     c.check_msg()
    #     #     # Then need to sleep to avoid 100% CPU usage (in a real
    #     #     # app other useful actions would be performed instead)
    #     #     time.sleep(1)
    #     c.check_msg()
    #     machine.idle()
    #     time.sleep(0.5)

    #c.disconnect()

run("192.168.0.112")