// MFRC522_BitBang.cpp
#include "MFRC522_BitBang.h"
#include "BitBangSPI.h"

// --- MFRC522 Register Definitions ---
#define CommandReg       0x01
#define ComIEnReg        0x02
#define DivIEnReg        0x03
#define ComIrqReg        0x04
#define DivIrqReg        0x05
#define ErrorReg         0x06
#define FIFODataReg      0x09
#define FIFOLevelReg     0x0A
#define ControlReg       0x0C
#define BitFramingReg    0x0D
#define ModeReg          0x11
#define TxModeReg        0x12
#define RxModeReg        0x13
#define TxControlReg     0x14
#define TxASKReg         0x15
#define CRCResultRegL    0x22
#define CRCResultRegH    0x21
#define ModWidthReg      0x24
#define TModeReg         0x2A
#define TPrescalerReg    0x2B
#define TReloadRegH      0x2C
#define TReloadRegL      0x2D
#define VersionReg       0x37

#define PCD_Idle         0x00
#define PCD_CalcCRC      0x03
#define PCD_Transceive   0x0C
#define PCD_SoftReset    0x0F

static uint8_t activeSSPin = 33;

void setActiveSSPin(uint8_t ssPin) {
  activeSSPin = ssPin;
}

void writeRegister(uint8_t reg, uint8_t value) {
  for (uint8_t j = 0; j < NUM_READERS; j++) {
    digitalWrite(SS_PINS[j], HIGH);
  }
  digitalWrite(activeSSPin, LOW);
  spiTransfer((reg << 1) & 0x7E);
  spiTransfer(value);
  digitalWrite(activeSSPin, HIGH);
}

uint8_t readRegister(uint8_t reg) {
  for (uint8_t j = 0; j < NUM_READERS; j++) {
    digitalWrite(SS_PINS[j], HIGH);
  }
  digitalWrite(activeSSPin, LOW);
  spiTransfer(((reg << 1) & 0x7E) | 0x80);
  uint8_t val = spiTransfer(0);
  digitalWrite(activeSSPin, HIGH);
  return val;
}

void setBitMask(uint8_t reg, uint8_t mask) {
  writeRegister(reg, readRegister(reg) | mask);
}

void clearBitMask(uint8_t reg, uint8_t mask) {
  writeRegister(reg, readRegister(reg) & (~mask));
}

bool isNewCardPresent() {
  writeRegister(CommandReg, PCD_Idle);
  writeRegister(ComIrqReg, 0x7F);
  writeRegister(FIFOLevelReg, 0x80);
  writeRegister(BitFramingReg, 0x07);
  writeRegister(FIFODataReg, 0x26);
  writeRegister(CommandReg, PCD_Transceive);
  setBitMask(BitFramingReg, 0x80);

  for (uint16_t i = 0; i < 1000; i++) {
    if (readRegister(ComIrqReg) & 0x30) break;
    delayMicroseconds(10);
  }

  uint8_t error = readRegister(ErrorReg);
  if (error & 0x1B) return false;

  return readRegister(FIFOLevelReg) == 2;
}

void calculateCRC(byte *data, byte length, byte *result) {
  writeRegister(CommandReg, PCD_Idle);
  writeRegister(DivIrqReg, 0x04);
  writeRegister(FIFOLevelReg, 0x80);
  for (byte i = 0; i < length; i++) {
    writeRegister(FIFODataReg, data[i]);
  }
  writeRegister(CommandReg, PCD_CalcCRC);
  uint32_t timeout = millis() + 10;
  while (!(readRegister(DivIrqReg) & 0x04)) {
    if (millis() > timeout) return;
  }
  result[0] = readRegister(CRCResultRegL);
  result[1] = readRegister(CRCResultRegH);
}

bool transceive(byte *sendData, byte sendLen, byte *backData, byte *backLen, byte *validBits = nullptr) {
  writeRegister(CommandReg, PCD_Idle);
  writeRegister(ComIrqReg, 0x7F);
  writeRegister(FIFOLevelReg, 0x80);

  for (byte i = 0; i < sendLen; i++) {
    writeRegister(FIFODataReg, sendData[i]);
  }

  writeRegister(CommandReg, PCD_Transceive);
  writeRegister(BitFramingReg, 0x80);

  uint32_t timeout = millis() + 36;
  while (!(readRegister(ComIrqReg) & 0x30)) {
    if (millis() > timeout) return false;
  }

  if (readRegister(ErrorReg) & 0x13) return false;

  byte len = readRegister(FIFOLevelReg);
  if (len > *backLen) return false;
  *backLen = len;
  for (byte i = 0; i < len; i++) {
    backData[i] = readRegister(FIFODataReg);
  }

  if (validBits) *validBits = readRegister(ControlReg) & 0x07;
  return true;
}

void haltCard() {
  byte cmd[] = {0x50, 0x00};
  byte crc[2];
  calculateCRC(cmd, 2, crc);
  byte buffer[4] = {cmd[0], cmd[1], crc[0], crc[1]};
  byte dummy[10];
  byte dummyLen = sizeof(dummy);
  transceive(buffer, 4, dummy, &dummyLen);
}

bool readCardUID(byte *uid, byte &uidLength) {
  byte buffer[10];
  byte bufferSize = sizeof(buffer);
  byte validBits = 0;
  byte anticollision_cmd[] = {0x93, 0x20};

  if (!transceive(anticollision_cmd, 2, buffer, &bufferSize, &validBits)) {
    Serial.println("Anti-collision failed");
    return false;
  }

  if (bufferSize != 5) {
    Serial.println("Invalid UID length");
    return false;
  }

  for (int i = 0; i < 4; i++) {
    uid[i] = buffer[i];
  }
  uidLength = 4;
  return true;
}

void initializeReader(uint8_t ssPin) {
  for (uint8_t j = 0; j < NUM_READERS; j++) {
    digitalWrite(SS_PINS[j], HIGH);
  }
  digitalWrite(ssPin, LOW);  // Only after releasing others
  activeSSPin = ssPin;
  writeRegister(CommandReg, PCD_SoftReset);
  delay(50);
  writeRegister(TxModeReg, 0x00);
  writeRegister(RxModeReg, 0x00);
  writeRegister(ModWidthReg, 0x26);
  writeRegister(TModeReg, 0x80);
  writeRegister(TPrescalerReg, 0xA9);
  writeRegister(TReloadRegH, 0x03);
  writeRegister(TReloadRegL, 0xE8);
  writeRegister(TxASKReg, 0x40);
  writeRegister(ModeReg, 0x3D);
  setBitMask(TxControlReg, 0x03);

  byte version = readRegister(VersionReg);
  Serial.print("Reader on SS ");
  Serial.print(ssPin);
  Serial.print(" Version: 0x");
  Serial.println(version, HEX);
}

const uint8_t NUM_READERS = 7;
const uint8_t SS_PINS[NUM_READERS] = {33, 34, 35, 36, 37, 38, 39};
