import os
import utime as time
from lib.ntp import Ntp

def _isDirectotyExist(dirname):
    is_exist = False
    try:
        tmp = os.stat(dirname)
        is_exist = True
    except OSError:
        is_exist = False
    return is_exist

def _CreateDirectoryIfNotExist(dirname):
    if not _isDirectotyExist(dirname):
        os.mkdir(dirname)

def _genFileName(path):
    fileName = '1.txt'
    logFiles = os.listdir(path)
    fileCount = len(logFiles)
    if fileCount > 0:
        last_file = logFiles[fileCount - 1]
        fileName = str(int(last_file.split('.')[0]) + 1) + '.txt'
    return path + '/' + fileName


class Log:
    def __init__(self, setting, filename = None):
        self._setting = setting
        self._path = setting.log_path       
        self.check()
        if self._setting.log_enable:
            if filename:
                self._filename = filename
            else:
                self._filename = _genFileName(self._path)

    def cleanfiles(self):
        logFiles = os.listdir(self._path)

    def check(self):
        if self._setting.log_enable:
            _CreateDirectoryIfNotExist(self._path)
            self.cleanfiles()
    
    def log(self, message):
        if self._setting.log_enable:
            self._file = open(self._filename, 'a')
            self._file.write(message + "\n")
            self._file.close()
        else:
            print(message)

    def close(self):
        self._file.close()