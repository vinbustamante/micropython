import lib.fs as fs
import ujson as json

class Setting:
    def __init__(self, filename):
        self._filename = filename
        setting = json.loads(fs.readfile(filename))

        #wifi settings
        self.wifi_ssid = setting['wifi']['ssid']
        self.wifi_pwd = setting['wifi']['pwd']

        #mqtt
        mqtt_value = setting['mqtt']
        self.mqtt_client_id = mqtt_value['client_id']
        self.mqtt_hostname = mqtt_value['hostname']
        self.mqtt_port = mqtt_value['port']
        self.mqtt_username = mqtt_value.get('username')
        self.mqtt_password = mqtt_value.get('password')
        self.mqtt_isSecured = mqtt_value['isSecured']
        self.mqtt_ssl_params = mqtt_value['ssl_params']

        #log
        log = setting['log']
        self.log_enable = log['isEnable']
        self.log_path = log['path']
        self.log_max_filecount= log['max_filecount']
    