import mysql.connector as connector


class DbClass:
    def __init__(self):

        self.__dsn = {
            "host": "localhost",
            "user": "root",
            "passwd": "XgLMCD",
            "db": "weather_station"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def get_types(self):
        self.__cursor.callproc('return_type')
        result = []
        for a in self.__cursor.stored_results():
            result.append(a.fetchall())
        return result

    def add_measurement(self, value, type):
        self.__cursor.callproc('add_measurement', [type, value])
        self.__connection.commit()

    def read_measurement(self, datetime_start, datetime_stop, type):
        self.__cursor.callproc('read_measurement', [datetime_start, datetime_stop, type])
        result = []
        for a in self.__cursor.stored_results():
            result.append(a.fetchall())
        return result

    def get_measurement_dates(self, datetime_start, datetime_stop):
        self.__cursor.callproc('get_measurement_date', [datetime_start, datetime_stop])
        result = []
        for a in self.__cursor.stored_results():
            result.append(a.fetchall())
        return result[0]



        # def getDataFromDatabase(self):
        #     # Query zonder parameters
        #     sqlQuery = "SELECT * FROM type"
        #
        #     self.__cursor.execute(sqlQuery)
        #     result = self.__cursor.fetchall()
        #     self.__cursor.close()
        #     return result
        #
        # def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
        #     # Query met parameters
        #     sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
        #     # Combineren van de query en parameter
        #     sqlCommand = sqlQuery.format(param1=voorwaarde)
        #
        #     self.__cursor.execute(sqlCommand)
        #     result = self.__cursor.fetchall()
        #     self.__cursor.close()
        #     return result
        #
        # def setDataToDatabase(self, value1):
        #     # Query met parameters
        #     sqlQuery = "INSERT INTO tablename (columnname) VALUES ('{param1}')"
        #     # Combineren van de query en parameter
        #     sqlCommand = sqlQuery.format(param1=value1)
        #
        #     self.__cursor.execute(sqlCommand)
        #     self.__connection.commit()
        #     self.__cursor.close()
