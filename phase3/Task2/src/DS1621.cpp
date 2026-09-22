#include "DS1621.h"
#include <Wire.h>

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
