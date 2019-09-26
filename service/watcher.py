import time
import machine
from machine import Timer
from machine import Timer

class Watcher:
    def __init__(self, logService, interval = 15, timerId = 1):
        self._logService = logService
        self._isStuck = False
        self._interval = interval * 1000 # in seconds
        self._timerId = timerId
        self._logService.log('Watcher : interval ' + str(interval) + ' seconds')
        
    def check(self):
        self._logService.log('Watcher : isProcess stuck ' + str(self._isStuck))
        if self._isStuck:
            self._logService.log('Watcher: process detected stuck. Will restart now')
            machine.reset()

    def run(self):
        self._timer = Timer(self._timerId)
        self._timer.init(mode=Timer.PERIODIC, period=self._interval, callback=lambda x: self.check())   # one shot firing after 1000ms

    def watch(self, func):
        if func:
            self._isStuck = True
            result = func() # the function should finish with the elapse time otherwise the device will restart
            self._isStuck = False
            return result