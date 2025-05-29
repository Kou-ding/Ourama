#include <SPI.h>
#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>
#include <nRF24L01.h>
#include <RF24.h>

#define PLAYER_ID 2 // Player ID for the RFID reader
// Declare the slave select (SS) pin (GPIO 5) for the RFID reader
MFRC522DriverPinSimple ss_pin(5);

// Initializes the SPI driver and the MFRC522 object for the RFID module
MFRC522DriverSPI driver{ss_pin}; // Create SPI driver
MFRC522 mfrc522{driver};         // Create MFRC522 instance

// Creates a pointer to a secondary SPI bus (HSPI), used for the nRF24L01
SPIClass * hspi = new SPIClass(HSPI);

// Defines CE and CSN pins for the nRF24L01 module
#define CE_PIN   4
#define CSN_PIN 15

// Creates a radio object using defined control pins
RF24 radio(CE_PIN, CSN_PIN);  // CE, CSN

// Defines a pipe address (5 characters + null terminator) for nRF24L01 communication
const byte address[6]="00001";

void setup() {
  // Starts serial communication and waits until it's ready.
  Serial.begin(9600);
  while(!Serial);

  // Initializes the RFID reader and prints its firmware version
  mfrc522.PCD_Init();
  MFRC522Debug::PCD_DumpVersionToSerial(mfrc522, Serial);
  Serial.println(F("Scan PICC to see UID"));

  // Starts the HSPI with custom pin numbers:
  // SCK=14, MISO=12, MOSI=13, SS=15
  // Initializes the radio object using the hspi bus
  hspi->begin(14, 12, 13, 15);
  radio.begin(hspi);

  // Checks if the radio is working; if not, it halts the program.
  if (!radio.begin()) {
    Serial.println("nRF24L01 not responding!");
    while (1);
  }

  // Configures the nRF24L01
  // Writing pipe
  radio.openWritingPipe(address);
  // Power level: Minimum
  radio.setPALevel(RF24_PA_MIN);
  // Data rate: 1 Mbps
  radio.setDataRate(RF24_250KBPS);
  // Channel 108
  radio.setChannel(108);
  // Disable the radio auto-acknowledgment
  radio.setAutoAck(true);
  radio.enableDynamicPayloads();
  // Retries 5 times, 15 delay units
  radio.setRetries(5, 15);
  // Sets the module to transmit mode
  radio.stopListening(); 
}

void loop() {
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if (!mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards.
	if (!mfrc522.PICC_ReadCardSerial()) {
		return;
	}

  // Prints the UID to the serial monitor.
  Serial.print("Card UID: ");
  MFRC522Debug::PrintUID(Serial, (mfrc522.uid));
  Serial.println();

  // Save the UID on a String variable
  String uidString = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) {
      uidString += "0"; 
    }
    uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println(uidString);
  
  // Stops communication with the current card.
  mfrc522.PICC_HaltA(); // Halt PICC

  // Short delay before transmission.
  delay(500);
  
  // Create a buffer with "player 1: " prefix
  char transmissionBuffer[25] = {0};  // Large enough for prefix + UID + null terminator
  sprintf(transmissionBuffer, "Player %d: ", PLAYER_ID);  
  strcat(transmissionBuffer, uidString.c_str());

  // Sends the combined buffer via nRF24L01
  bool success = radio.write(&transmissionBuffer, sizeof(transmissionBuffer));

  // Prints success or failure message.
  if (success) {
    Serial.print("Transmission successful!\n");
    Serial.print("Contents:\n");
    Serial.println(transmissionBuffer);
  } else {
    Serial.println("Transmission failed!");
    radio.printDetails();
  }
   // Waits 1 second before checking for a new card.
   delay(1000);
}
