// MFRC522_BitBang.h
#pragma once
#include <Arduino.h>

extern const uint8_t NUM_READERS;
extern const uint8_t SS_PINS[];

void initializeReader(uint8_t ssPin);
bool isNewCardPresent();
bool readCardUID(byte *uid, byte &uidLength);
void haltCard();
void setActiveSSPin(uint8_t ssPin);
void writeRegister(uint8_t reg, uint8_t value);
uint8_t readRegister(uint8_t reg);