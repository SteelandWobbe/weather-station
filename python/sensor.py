# import serial
import time


class Sensor:
    def __init__(self):
        self._ser = serial.Serial('/dev/ttyUSB0', 9600)  # DELAY OF ~2s REQUIRED BEFORE READING
        time.sleep(2)

    def get_data_arduino(self):
        self._ser.write(b'a')
        return self._ser.readline()[:-1].decode('ascii').split(';')
