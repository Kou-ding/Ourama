#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Creates an RF24 object
RF24 radio(9, 10); // 9 -> CE (Chip Enable pin), 10 -> CSN (Chip Select Not pin)

// This is the pipe address
const byte address[6] = "00001";

void setup() {
  // Initializes serial communication at 9600 baud
  Serial.begin(9600);
  // Initializes the nRF24L01 radio
  radio.begin();
  // Opens reading pipe 0 using the specified address
  radio.openReadingPipe(0, address);
  // Sets transmission power level to minimum (for short-range)
  radio.setPALevel(RF24_PA_MIN);
  // Sets data rate to 1 Megabit per second.
  radio.setDataRate(RF24_250KBPS); // Better range and reliability
  // Sets RF channel (frequency = 2.408 GHz)
  radio.setChannel(108);
  // Disable the radio auto-acknowledgment
  radio.setAutoAck(true);
  radio.enableDynamicPayloads();
  // Puts the nRF24L01 module into receive mode
  radio.startListening();
}

void loop() {
  // Declares a buffer receivedUID to store up to 24 characters + null terminator
  char receivedUID[25]={0};
  // Checks if data is available from the radio module
  if (radio.available())  {
    // Reads the incoming data into the buffer
    radio.read(&receivedUID, sizeof(receivedUID));
    // Prints the received UID to the Serial Monitor
    Serial.println(receivedUID);
    // Clears the RX buffer to avoid reading the same message multiple times
    //radio.flush_rx(); // Might interfere with with the ACK
  }
}