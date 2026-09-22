#include <Arduino.h>
#include <Wire.h>

#define TEMP_SENSOR_ADDR 0x48
#define REG_ACCESS_CONFIG 0xAC
#define REG_START_CONVERT 0xEE
#define REG_READ_TEMP 0xAA

enum I2C_Status_t {
  I2C_OK = 0,
  I2C_ERR_TOO_LONG = 1,
  I2C_ERR_ADDR_NACK = 2,
  I2C_ERR_DATA_NACK = 3,
  I2C_ERR_BUS = 4,
  I2C_ERR_TIMEOUT = 5,
  I2C_ERR_READ_SHORT = 6
};

I2C_Status_t WriteRegister(uint8_t devAddr, uint8_t regAddr, uint8_t data) {
  Wire.beginTransmission(devAddr);

  Wire.write(regAddr);
  Wire.write(data);

  return (I2C_Status_t)Wire.endTransmission();
}

I2C_Status_t WriteRegister(uint8_t devAddr, uint8_t regAddr) {
  Wire.beginTransmission(devAddr);

  Wire.write(regAddr);

  return (I2C_Status_t)Wire.endTransmission();
}

I2C_Status_t ReadRegister(uint8_t devAddr, uint8_t regAddr, uint8_t *dataDest,
                          uint8_t length) {
  Wire.beginTransmission(devAddr);
  Wire.write(regAddr);

  uint8_t status = Wire.endTransmission(false);
  if (status != I2C_OK) {
    return (I2C_Status_t)status;
  }

  uint8_t bytesReceived = Wire.requestFrom(devAddr, length);
  if (bytesReceived != length) {
    return I2C_ERR_READ_SHORT;
  }

  for (uint8_t i = 0; i < length; i++) {
    dataDest[i] = Wire.read();
  }

  return I2C_OK;
}

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