#include <SPI.h>
#include <RF24Network.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN
RF24Network network(radio);// Include the radio in the network
const uint16_t this_node = 00;   // Address of our node in Octal format 

void setup() {
  Serial.begin(9600); 
  radio.begin(); 
  network.begin(108, this_node);   // (channel, node address)
  radio.setDataRate(RF24_250KBPS); // Match transmitter radio.setPALevel(RF24_PA_MIN);
  radio.setPALevel(RF24_PA_MIN);   // Match transmitter (optional, but good for consistency)
  radio.enableDynamicPayloads(); 
}

void loop() {

  network.update();  // Process incoming network traffic

  while ( network.available() ) {              // If there's any data
    RF24NetworkHeader header;
    char text[40] = "";
    network.read(header, &text, sizeof(text)); // Read the data packet
    Serial.println(text); 
  }
  delay(200);
}