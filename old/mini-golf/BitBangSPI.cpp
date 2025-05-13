// BitBangSPI.cpp
#include "BitBangSPI.h"

const uint8_t MOSI_PIN = 30;
const uint8_t MISO_PIN = 31;
const uint8_t SCK_PIN  = 32;

void spiBegin() {
  pinMode(MOSI_PIN, OUTPUT);
  pinMode(MISO_PIN, INPUT);
  pinMode(SCK_PIN, OUTPUT);
  digitalWrite(SCK_PIN, LOW);
}

uint8_t spiTransfer(uint8_t dataOut) {
  uint8_t dataIn = 0;
  for (int i = 7; i >= 0; i--) {
    digitalWrite(MOSI_PIN, (dataOut >> i) & 1);
    delayMicroseconds(1);
    digitalWrite(SCK_PIN, HIGH);
    delayMicroseconds(2);
    dataIn <<= 1;
    dataIn |= digitalRead(MISO_PIN);
    digitalWrite(SCK_PIN, LOW);
    delayMicroseconds(1);
  }
  return dataIn;
}
