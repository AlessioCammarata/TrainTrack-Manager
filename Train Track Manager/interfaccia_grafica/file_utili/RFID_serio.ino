#define DEBUG

#include <SPI.h>
#include <MFRC522.h>

const byte numReaders = 8;

const byte ssPins[] = {4, 5, 6, 7, 8, 9, 10, 18};
const byte resetPin = 2;
String read = "";
String readRFID = "1";
uint8_t id = 10;
MFRC522 mfrc522[numReaders];


void setup() {

  //#ifdef DEBUG
  Serial.begin(115200);
  //Serial.println(F("Serial communication started"));

  SPI.begin();

  for (uint8_t i=0; i<numReaders; i++){
    mfrc522[i].PCD_Init(ssPins[i],resetPin);

    // Serial.print(F("Reader #"));
    // Serial.println(i);

    // Serial.print(F("sul pin "));
    // Serial.println(String(ssPins[i]));

    // mfrc522[i].PCD_GetAntennaGain();
    delay(100);
  }
  //Serial.println("End");
}

void loop() {

  for (uint8_t i=0;i<numReaders;i++){
    //Iniizializzare il sensore
    mfrc522[i].PCD_Init();

    if (mfrc522[i].PICC_IsNewCardPresent() && mfrc522[i].PICC_ReadCardSerial()) {
      readRFID = dump_byte_array(mfrc522[i].uid.uidByte, mfrc522[i].uid.size);
      if (read != readRFID or id != i){
        Serial.print(i+1);
        Serial.println("/" + readRFID);
        read = readRFID;
        id = i;
      }
      break;
    }

      // mfrc522[i].PICC_HaltA();
      // mfrc522[i].PCD_StopCrypto1();
     
  }
  
}

String dump_byte_array(byte *buffer, byte bufferSize) {
  String result = "";
  for (byte i = 0; i < bufferSize; i++) {
    //result += (buffer[i] < 0x10 ? " 0" : " ");
    result += String(buffer[i], HEX);
  }
  return result;
}