import machine
import time
from lib.wlan import Wifi
from lib.umqttsimple import MQTTClient
from lib.pin import Led
import socket
import network
import ussl as ssl

led = Led(2)

wifi = Wifi('Redbean_24GHZ','homeboys')
wifi.connect()
while not wifi.is_connected():
    machine.idle()
    time.sleep(1)    
print('wifi connected')
#print(wifi._wlan.ifconfig())

# CA_FILE = 'cert/ca.crt';
# KEY_FILE = 'cert/device001.key'
# CERT_FILE = 'cert/device001.crt'

# CA_CONTENT = ''
# KEY_CONTENT = ''
# DEVICE_CERT = ''

# with open(KEY_FILE) as f:
#     KEY_CONTENT = f.read()
# with open(CERT_FILE) as f:
#     DEVICE_CERT = f.read()
# with open(CA_FILE) as f:
#     CA_CONTENT = f.read()

def message_receive(topic, payload):
    print(topic, payload)
    if payload == b'1':
        print('light on')
        led.on()
    else:
        print('light off')
        led.off()

def run(server):
    #c = MQTTClient("umqtt_client", server, port=8883,ssl = True, ssl_params={})    
    #c = MQTTClient("umqtt_client", server, port=8883, ssl_params={"ca_certs":"/flash/cert/ca.crt", "certfile":"/flash/cert/device001.crt", "keyfile":"/flash/cert/device001.key", ssl_version:3})
    c = MQTTClient("umqtt_client", server, port=8883, user='marvin',password='redfield', ssl = True, ssl_params={})
    #c = MQTTClient("umqtt_client", server, port=8883, ssl=True, ssl_params={"cert_reqs": ssl.CERT_REQUIRED,"certfile":"cert/device001.crt", "keyfile":"cert/device001.key", "ca_certs":"cert/ca.crt"})
    #c = MQTTClient("umqtt_client", server, port=8883, keepalive=10000, ssl=True, ssl_params={"key": KEY_CONTENT, "cert": DEVICE_CERT, "server_side": True})
    c.set_callback(message_receive)
    c.connect()
    print('Connected now')
    c.subscribe(b"home/livingroom/temperature")
    while True:
        # if True:
            # Blocking wait for message
        #c.wait_msg()
        # else:
        #     # Non-blocking wait for message
        #     c.check_msg()
        #     # Then need to sleep to avoid 100% CPU usage (in a real
        #     # app other useful actions would be performed instead)
        #     time.sleep(1)
        
        #blocking
        c.wait_msg()
        
        # c.check_msg()
        # machine.idle()
        # time.sleep(0.5)

    #c.disconnect()

#run("vinbustamante.dlinkddns.com")
run("192.168.0.112")

#print(dir(ssl))

#print(socket.getaddrinfo('vinbustamante.dlinkddns.com', 8883))
