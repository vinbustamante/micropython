from lib.wlan import Wifi
import machine
import time


def connect(setting, logService):
    logService.log('will connect to ' + setting.wifi_ssid)
    wifi = Wifi(setting.wifi_ssid,setting.wifi_pwd)
    logService.log('Network connection will start connecting')
    wifi.connect()
    logService.log('Successfully established network connection')
    attemp = 1
    while not wifi.is_connected():
        logService.log('Network connection attemp ' + str(attemp))
        machine.idle()
        time.sleep(1)
    logService.log('Successfully connected to ' + setting.wifi_ssid)