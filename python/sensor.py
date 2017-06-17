import serial
import time
from DbClass import DbClass

supersample = 1  # amount of samples to take for each measurement
delay = 10  # delay in seconds between measurements; 900s=15min
_samplespeed = delay / supersample  # time in between measurements; 900/15=60

time.sleep(5)                              # letting the Arduino boot

db = DbClass()

ser = serial.Serial('/dev/ttyUSB0', 9600)  # DELAY OF ~2s REQUIRED BEFORE READING
time.sleep(2)


def get_data_arduino():
    ser.write(b'a')
    return ser.readline()[:-1].decode('ascii').split(';')


get_data_arduino()                      # update display

while True:
    temp = []
    hum = []
    light = []
    for i in range(0, supersample):
        data = get_data_arduino()
        temp.append(float(data[0]))
        hum.append(float(data[1]))
        light.append(float(data[2])*1.1)                # plexiglas lets trough ca. 90% of light
        time.sleep(_samplespeed)

    temp_avg = sum(temp) / supersample  # calculate average
    hum_avg = sum(hum) / supersample
    light_avg = sum(light) / supersample

    db.add_measurement(value=temp_avg, type=1)  # update database with averages
    db.add_measurement(value=hum_avg, type=2)
    db.add_measurement(value=light_avg, type=4)
