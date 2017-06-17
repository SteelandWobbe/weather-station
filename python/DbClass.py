import mysql.connector as connector


class DbClass:
    def __init__(self):

        self.__dsn = {
            "host": "localhost",
            "user": 'a',
            "passwd": 'YOKZb6ce109QYRXSArnh',
            "db": "weather_station"
        }
        self.__connection = connector.connect(**self.__dsn)

    def get_types(self):
        cursor = self.__connection.cursor()
        cursor.callproc('return_type')
        result = []
        for a in cursor.stored_results():
            result.append(a.fetchall())
        self.__connection.commit()
        cursor.close()
        return result

    def add_measurement(self, value, type):
        cursor = self.__connection.cursor()
        cursor.callproc('add_measurement', [type, value])
        self.__connection.commit()
        cursor.close()

    def read_measurement(self, datetime_start, datetime_stop, type):
        cursor = self.__connection.cursor()
        cursor.callproc('read_measurement', [datetime_start, datetime_stop, type])
        result = []
        for a in cursor.stored_results():
            result.append(a.fetchall())
        self.__connection.commit()
        cursor.close()
        return result

    def get_measurement_dates(self, datetime_start, datetime_stop):
        cursor = self.__connection.cursor()
        cursor.callproc('get_measurement_date', [datetime_start, datetime_stop])
        result = []
        for a in cursor.stored_results():
            result.append(a.fetchall())
        self.__connection.commit()
        cursor.close()
        return result[0]

    def get_last_measurement(self, type):
        cursor = self.__connection.cursor()
        cursor.callproc('get_last_measurement', [type])
        result = []
        for a in cursor.stored_results():
            result.append(a.fetchall())
        self.__connection.commit()
        cursor.close()
        return result[0]

    def add_user(self, username, password_hash):
        cursor = self.__connection.cursor()
        cursor.callproc('add_user', [username, password_hash])
        self.__connection.commit()
        cursor.close()

    def get_password_user(self, username):
        cursor = self.__connection.cursor()
        cursor.callproc('get_password_user', [username])
        result = []
        for a in cursor.stored_results():
            result.append(a.fetchall())
        self.__connection.commit()
        cursor.close()
        return result[0][0][0]

    def update_password_user(self, username, new_hashed_password):
        cursor = self.__connection.cursor()
        cursor.callproc('update_password_user', [username, new_hashed_password])
        self.__connection.commit()
        cursor.close()
