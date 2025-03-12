#include<SPI.h>
#include<MFRC522.h>

//creating mfrc522 instance
#define RSTPIN 9
#define SSPIN_1 10
#define SSPIN_2 8
MFRC522 rfid1(SSPIN_1, RSTPIN);
MFRC522 rfid2(SSPIN_2, RSTPIN);

byte readcard[4]; //stores the UID of current tag which is read

bool first = false;

void setup() {
  Serial.begin(9600);

  SPI.begin();

  if (first) {
    rfid1.PCD_Init(); //initialize the receiver  
    rfid1.PCD_DumpVersionToSerial(); //show details of card reader module
  } else {
    rfid2.PCD_Init();
    rfid2.PCD_DumpVersionToSerial();
  }

  Serial.println(F("Scan Access Card to see Details"));
}


void loop() {
  if (first) { // FIRST READER
    if(!rfid1.PICC_IsNewCardPresent()){
      return 0;
    }
    if(!rfid1.PICC_ReadCardSerial()){
      return 0;
    }
    
    Serial.println("THE UID OF THE SCANNED CARD IS:");
    
    for(int i=0;i<4;i++){
      readcard[i]=rfid1.uid.uidByte[i]; //storing the UID of the tag in readcard
      Serial.print(readcard[i],HEX);
      
    }
    Serial.println("");
    rfid1.PICC_HaltA();
  } else { // SECOND READER
    // rfid2.PICC_IsNewCardPresent();
    // rfid2.PICC_ReadCardSerial();

    if(!rfid2.PICC_IsNewCardPresent()){
      // Serial.println("Here1");
      return 0;
    }
    if(!rfid2.PICC_ReadCardSerial()){
      // Serial.println("Here2");
      return 0;
    }
    
    Serial.println("THE UID OF THE SCANNED CARD IS:");
    
    for(int i=0;i<4;i++){
      readcard[i]=rfid2.uid.uidByte[i]; //storing the UID of the tag in readcard
      Serial.print(readcard[i],HEX);
      
    }
    Serial.println("");
    rfid2.PICC_HaltA();
  }
}
