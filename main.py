import time
from lib.umqttsimple import MQTTClient
from service.setting import Setting
import service.network as networkService
import service.log as log
import service.message_processor as messageProcessor
from service.watcher import Watcher
from lib.pin import Led
import lib.util as util
import dht
from machine import ADC
import onewire, ds18x20, machine

#CONSTANT
CONFIG = 'conf/config.json'
setting = Setting(CONFIG)
logService = log.Log(setting)
#dht11 = dht.DHT11(machine.Pin(4))
dht11 = dht.DHT11(machine.Pin(2))
adc = ADC(0)

data = machine.Pin(14)
ds = ds18x20.DS18X20(onewire.OneWire(data))
roms = ds.scan()


SERVICEBUS_SWITCH1_TOPIC = 'device/' + setting.mqtt_client_id + '/switch/1'
SERVICEBUS_BUZZER = 'device/' + setting.mqtt_client_id + '/buzzer'
SERVICEBUS_REGISTER_ADDRESS = 'device/registration'
SERVICEBUS_SENSOR_VALUE = 'device/' + setting.mqtt_client_id + '/values'

watcher = Watcher(logService, 45)
watcher.run()

led = Led(0)
buzzer = Led(12)

def message_receive(topic, payload):
    str_topic = util.bytesToString(topic)    
    if str_topic == SERVICEBUS_SWITCH1_TOPIC:
        if payload == b'1':
            led.on()
        else:
            led.off()
    elif str_topic == SERVICEBUS_BUZZER:
        if payload == b'1':
            buzzer.on()
        else:
            buzzer.off()
    
def connectToNetwork():
    networkService.connect(setting, logService)

def createMessageBus():
    client = MQTTClient(setting.mqtt_client_id, setting.mqtt_hostname, 1883, user='marvin', password='redfield')
    #client = MQTTClient(setting.mqtt_client_id, setting.mqtt_hostname, 1883)
    #client = MQTTClient(setting.mqtt_client_id, setting.mqtt_hostname, 1883)
    #client = MQTTClient(setting.mqtt_client_id, '192.168.0.105', 8883, ssl= True, ssl_params={"ca_certs":'/flash/certs/ca.pem', "certfile":"/flash/certs/esp.crt"})
    client.set_callback(message_receive)
    client.connect(clean_session=True)
    client.subscribe(util.stringToBytes(SERVICEBUS_SWITCH1_TOPIC))
    client.subscribe(util.stringToBytes(SERVICEBUS_BUZZER))

    #register the device
    deviceInfo = {"id": setting.mqtt_client_id }
    client.publish(util.stringToBytes(SERVICEBUS_REGISTER_ADDRESS), util.toJson(deviceInfo))
    return client    

while True:
    try:
        watcher.watch(connectToNetwork)
        time.sleep(1) # wait for wifi
        client = watcher.watch(createMessageBus)
        while True:
            logService.log('Main: checking message')
            watcher.watch(lambda : client.check_msg())
            time.sleep(1)
            lightIntensity = adc.read()
            dht11.measure()
            ds.convert_temp()
            json = util.toJson({"temp": dht11.temperature(), "hum": dht11.humidity(), "light": lightIntensity, "temp2":  ds.read_temp(roms[0])})
            client.publish(util.stringToBytes(SERVICEBUS_SENSOR_VALUE), json)
    except Exception as e:
        logService.log('an error was encountered.' + str(e))
        time.sleep(3)