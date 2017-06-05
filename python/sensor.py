import serial
import time
import DbClass

class Sensor:
    def __init__(self):
        # self._ser = serial.Serial('/dev/ttyUSB0', 9600)  # DELAY OF ~2s REQUIRED BEFORE READING
        self._db = DbClass.DbClass()
        time.sleep(2)

    def _get_data_arduino(self):
        self._ser.write(b'a')
        return self._ser.readline()[:-1].decode('ascii').split(';')

    def write_data_to_db(self):
        # 1: temperature
        # 2: humidity
        # 3: pressure
        # 4: luminosity
        data = self._get_data_arduino()
        self._db.add_measurement(data[0], 1)
        self._db.add_measurement(data[1], 2)
        self._db.add_measurement(data[2], 4)

