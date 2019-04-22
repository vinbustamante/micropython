import network

class Wifi:
    def __init__(self, ssid = None, pwd = None):
        self._ssid = ssid
        self._ssid_pwd = pwd
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        #self._wlan.config('esp-cool')
    
    def connect(self, ssid = None, ssid_pwd = None):
        self._wlan.connect(ssid or self._ssid, ssid_pwd or self._ssid_pwd)

    def is_connected(self):
        return self._wlan.isconnected
    
    def ip(self):
        return self._wlan.ifconfig()[0]