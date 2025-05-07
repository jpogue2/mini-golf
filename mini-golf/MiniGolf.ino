#include "BitBangSPI.h"
#include "MFRC522_BitBang.h"

#define RST_PIN 48

void setup() {
  pinMode(RST_PIN, OUTPUT);
  digitalWrite(RST_PIN, HIGH);
  Serial.begin(9600);
  while (!Serial);
  Serial.println("--- SYSTEM BOOTING ---");

  spiBegin();
  for (uint8_t i = 0; i < NUM_READERS; i++) {
    pinMode(SS_PINS[i], OUTPUT);
    digitalWrite(SS_PINS[i], HIGH);
    initializeReader(SS_PINS[i]);
  }
}

void loop() {
  for (uint8_t i = 0; i < NUM_READERS; i++) {
    setActiveSSPin(SS_PINS[i]);
    byte uid[10];
    byte uidLength;

    if (isNewCardPresent()) {
      Serial.print("Card detected on reader ");
      Serial.println(i);

      if (readCardUID(uid, uidLength)) {
        Serial.print("UID: ");
        for (byte j = 0; j < uidLength; j++) {
          if (uid[j] < 0x10) Serial.print("0");
          Serial.print(uid[j], HEX);
          Serial.print(" ");
        }
        Serial.println();
      }

      haltCard();
    }
  }

  delay(200);
}
