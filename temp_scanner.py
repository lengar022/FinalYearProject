import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Read sensor name
def read_name():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()

# Read raw sensor data
def read_raw_data():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Parse the data
def read_temp():
    lines = read_raw_data()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_raw_data()
    
    idx = lines[1].find('t=')
    
    if idx != -1:
        temp_string = lines[1][idx+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
 
while True:
    print(' C=%3.3f'% read_temp())