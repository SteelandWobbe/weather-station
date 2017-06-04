import RPi.GPIO as GPIO
import serial
import time
import DbClass

ser = serial.Serial('/dev/ttyUSB0', 9600)
db = DbClass.DbClass()

# time.sleep(2)  # nodig vr serieel usb


def get_data_arduino():
    ser.write(b'a')
    return ser.readline()[:-1].decode('ascii').split(';')


def write_data_to_db():
    # 1: temperature
    # 2: humidity
    # 3: pressure
    # 4: luminosity
    data = get_data_arduino()
    # data = [25.74, 54.89, 14500]
    db.add_measurement(data[0], 1)
    db.add_measurement(data[1], 2)
    db.add_measurement(data[2], 4)


def read_data_db(datetime_start, datetime_stop, type):
    data = db.read_measurement(datetime_start, datetime_stop, type)
    result = []
    for a in data[0]:
        result.append(a[0])
    return result

# write_data_to_db()

print(read_data_db('2017-01-01', '2018-01-01', 1))
