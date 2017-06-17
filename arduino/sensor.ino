float temperature, humidity, light;

// DHT22
#include "DHT.h"
DHT dht(2, DHT22);   //DHT dht22(PIN, DHTTYPE)

// TSL2561
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 1);

//LCD
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x3f, 16, 4);


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
   // LCD
  lcd.begin();
}

void loop() {
  if (Serial.available()) {
    temperature = read_temp();
    humidity = read_humidity();
    light = read_light();
    Serial.print(String(temperature) + ";" + String(humidity) + ";" + String(light) + "\n");
    lcd.setCursor(0, 0);
    lcd.print("Temp: " + String(temperature));
    lcd.setCursor(0, 1);
    lcd.print("Rel. lv: " + String(humidity));
    lcd.setCursor(-4, 2);
    lcd.print("Licht: " + String(light));
    Serial.read();
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
