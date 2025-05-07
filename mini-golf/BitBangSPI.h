// BitBangSPI.h
#pragma once
#include <Arduino.h>

void spiBegin();
uint8_t spiTransfer(uint8_t dataOut);
extern const uint8_t MOSI_PIN, MISO_PIN, SCK_PIN;
