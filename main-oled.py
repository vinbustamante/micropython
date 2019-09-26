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
# from machine import ADC
import machine
import ssd1306
from machine import Timer
import onewire, ds18x20
from machine import ADC

#oled
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
isDisplayEnable = False
displayTimer = None


#CONSTANT
CONFIG = 'conf/config.json'
setting = Setting(CONFIG)
logService = log.Log(setting)
dht11 = dht.DHT11(machine.Pin(2))

# dallas
data = machine.Pin(14)
dallasTemp = ds18x20.DS18X20(onewire.OneWire(data))
roms = dallasTemp.scan()

# ldr
adc = ADC(0)

led = Led(0)
led.off()
buzzer = Led(12)
buzzer.off()

SERVICEBUS_SWITCH1_TOPIC = 'device/' + setting.mqtt_client_id + '/switch/1'
SERVICEBUS_BUZZER = 'device/' + setting.mqtt_client_id + '/buzzer'
SERVICEBUS_REGISTER_ADDRESS = 'device/registration'
SERVICEBUS_SENSOR_VALUE = 'device/' + setting.mqtt_client_id + '/values'
SERVICEBUS_DISPLAY = 'device/' + setting.mqtt_client_id + '/display'

watcher = Watcher(logService, 45)
watcher.run()

def message_receive(topic, payload):
    global isDisplayEnable
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
    elif str_topic == SERVICEBUS_DISPLAY:
        if payload == b'1':
            isDisplayEnable = True
        else:
            isDisplayEnable = False
    
def connectToNetwork():
    networkService.connect(setting, logService)

def createMessageBus():
    # client = MQTTClient(setting.mqtt_client_id, setting.mqtt_hostname, 1883)
    client = MQTTClient(setting.mqtt_client_id, setting.mqtt_hostname, 1883, user='marvin', password='redfield')
    client.set_callback(message_receive)
    client.connect(clean_session=True)
    client.subscribe(util.stringToBytes(SERVICEBUS_SWITCH1_TOPIC))
    client.subscribe(util.stringToBytes(SERVICEBUS_BUZZER))
    client.subscribe(util.stringToBytes(SERVICEBUS_DISPLAY))

    #register the device
    deviceInfo = {"id": setting.mqtt_client_id }
    client.publish(util.stringToBytes(SERVICEBUS_REGISTER_ADDRESS), util.toJson(deviceInfo))
    return client    

def displayOff(client):
    global displayTimer
    client.publish(util.stringToBytes(SERVICEBUS_DISPLAY), '0')
    displayTimer = None

while True:
    try:
        watcher.watch(connectToNetwork)        
        time.sleep(1) # wait for wifi
        client = watcher.watch(createMessageBus)
        while True:
            logService.log('Main: checking message')
            watcher.watch(lambda : client.check_msg())

            # convert reading
            dht11.measure()
            dallasTemp.convert_temp()
            lightIntensity = adc.read()

            if isDisplayEnable:
                if displayTimer == None:
                    displayTimer = Timer(2)
                    displayTimer.init(mode=Timer.ONE_SHOT, period = 5000, callback=lambda x: displayOff(client))
                oled.poweron()
                oled.fill(0)
                oled.text('temp : ' + str(dht11.temperature()), 0, 0)
                oled.text('hum : ' + str(dht11.humidity()), 0, 10)
                oled.text('temp2 : ' + str(dallasTemp.read_temp(roms[0])), 0, 20)
                oled.text('light : ' + str(lightIntensity), 0, 30)
                oled.show()
            else:
                oled.poweroff()

            json = util.toJson({"temp": dht11.temperature(), "hum": dht11.humidity(), "temp2": dallasTemp.read_temp(roms[0]), "light": lightIntensity  })
            client.publish(util.stringToBytes(SERVICEBUS_SENSOR_VALUE), json)

            if (lightIntensity <= 50):
                client.publish(util.stringToBytes(SERVICEBUS_DISPLAY), "1")
    
            time.sleep(1)

    except Exception as e:
        logService.log('an error was encountered.' + str(e))        
        oled.poweron()
        oled.fill(0)
        oled.text('Error ', 0, 0)
        oled.show()
        time.sleep(5)
