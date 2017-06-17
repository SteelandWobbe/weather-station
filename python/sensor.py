import serial
import time
from DbClass import DbClass

time.sleep(10)                              # letting the Arduino boot

db = DbClass()

ser = serial.Serial('/dev/ttyUSB0', 9600)  # DELAY OF ~2s REQUIRED BEFORE READING
time.sleep(2)


def get_data_arduino():
    ser.write(b'a')
    return ser.readline()[:-1].decode('ascii').split(';')

get_data_arduino()                      # update display

while True:
    data = get_data_arduino()
    temp = (float(data[0]))
    hum = (float(data[1]))
    light = (float(data[2])) 
    time.sleep(300)

    db.add_measurement(value=temp, type=1)  # update database with averages
    db.add_measurement(value=hum, type=2)
    db.add_measurement(value=light, type=4)
