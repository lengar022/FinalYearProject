import os
import glob

class TempMonitor:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        
        base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp_raw(self):
        with open(self.device_file, "r") as f:
            return f.readlines()

    def read_temp(self):
        lines = self.read_temp_raw()
        if lines[0].strip()[-3:] != 'YES':
            return None
        
        idx = lines[1].find('t=')
        
        if idx == -1:
            return None
        
        temp_string = lines[1][idx+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    