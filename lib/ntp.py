import ntptime
from machine import RTC

class Ntp:
    def __init__(self):
        self._rtc = RTC()

    def sync(self):
        tmp = ntptime.settime()
        return None

    def now(self):
        return self._rtc.datetime()