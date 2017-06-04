float temperature, humidity, pressure, light;


// DHT22
#include "DHT.h"
DHT dht(2, DHT22);   //DHT dht22(PIN, DHTTYPE)

// TSL2561
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 1);

// BME280
#include <stdint.h>
#include "SparkFunBME280.h"
#include "SPI.h"
BME280 bme;



void setup() {
  delay(50);  // making sure all sensors can start up
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
  // DHT22
  dht.begin();

  // TSL2561
  tsl.begin();
  tsl.enableAutoRange(true);
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);

  //BME280
  bme.settings.commInterface = I2C_MODE;
  bme.settings.I2CAddress = 0x76;
  bme.settings.runMode = 3;
  bme.settings.tStandby = 0;
  bme.settings.filter = 0;
  bme.settings.tempOverSample = 5;
  bme.settings.pressOverSample = 5;
  bme.settings.humidOverSample = 5;
  bme.begin();
}

void loop() {
  if (Serial.available()) {
    Serial.read();
    Serial.print(String(read_temp()) + ";" + String(read_humidity()) + ";" + String(read_light())/* + "," + String(read_pressure) */+ "\n");
    delay(500);
  }
}

float read_temp() {
  return dht.readTemperature();
}

float read_humidity() {
  return dht.readHumidity();
}

float read_light() {
  sensors_event_t event;
  tsl.getEvent(&event);
  return event.light;
}

float read_pressure() {
  return bme.readFloatPressure();
}
