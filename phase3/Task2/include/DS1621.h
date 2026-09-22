#ifndef DS1621_H
#define DS1621_H

#include <Arduino.h>

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

I2C_Status_t WriteRegister(uint8_t devAddr, uint8_t regAddr, uint8_t data);
I2C_Status_t WriteRegister(uint8_t devAddr, uint8_t regAddr);
I2C_Status_t ReadRegister(uint8_t devAddr, uint8_t regAddr, uint8_t *dataDest,
                          uint8_t length);

#endif
