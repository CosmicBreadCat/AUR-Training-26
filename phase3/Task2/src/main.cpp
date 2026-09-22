#include <Arduino.h>
#include <Wire.h>
#include "DS1621.h"

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // sensor config
  I2C_Status_t configStatus =
      WriteRegister(TEMP_SENSOR_ADDR, REG_ACCESS_CONFIG, 0x00);
  I2C_Status_t convertStatus =
      WriteRegister(TEMP_SENSOR_ADDR, REG_START_CONVERT);

  if (configStatus != I2C_OK || convertStatus != I2C_OK) {
    Serial.println("Error in setup");
    return;
  }

  // poll done bit
  uint8_t configByte;
  I2C_Status_t readStatus;
  int counter = 0;
  while (counter < 20) {
    readStatus =
        ReadRegister(TEMP_SENSOR_ADDR, REG_ACCESS_CONFIG, &configByte, 1);
    if (readStatus == I2C_OK && (configByte & (1 << 7))) {
      break;
    }
    delay(100);
    counter++;
  }

  if (counter >= 20) {
    Serial.print("Poll timeout - counter: ");
    Serial.print(counter);
    Serial.print(", readStatus: ");
    Serial.println(readStatus);

    return;
  }
}

void loop() {
  uint8_t tempBuffer[2];
  I2C_Status_t readStatus;

  readStatus = ReadRegister(TEMP_SENSOR_ADDR, REG_READ_TEMP, tempBuffer, 2);

  float tempC = (int8_t)tempBuffer[0] + ((tempBuffer[1] >> 7) * 0.5f);

  Serial.print("Status: ");
  Serial.print(readStatus);
  Serial.print(" | Temp: ");
  Serial.print(tempC);
  Serial.print(" | MSB: ");
  Serial.print(tempBuffer[0]);
  Serial.print(" | LSB: ");
  Serial.println(tempBuffer[1]);

  delay(500);
}
