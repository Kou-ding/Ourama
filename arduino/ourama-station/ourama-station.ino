/*
Arduino Wireless Communication Tutorial,
Example 1 - Receiver Code,
,
by Dejan Nedelkovski, www.HowToMechatronics.com,
,
Library: TMRh20/RF24, https://github.com/tmrh20/RF24/,
*/

#include <SPI.h>
#include <RF24Network.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN
RF24Network network(radio);// Include the radio in the network
const uint16_t this_node = 00;   // Address of our node in Octal format 

//const byte address[6] = "00001";

void setup() {
  Serial.begin(9600); 
  radio.begin(); 
  network.begin(108, this_node); //(channel, node address)
  //radio.setChannel(108); // Match transmitter
  radio.setDataRate(RF24_250KBPS); // Match transmitter radio.setPALevel(RF24_PA_MIN);
  radio.setPALevel(RF24_PA_MIN); // Match transmitter (optional, but good for consistency)
  radio.enableDynamicPayloads(); 
  //radio.openReadingPipe(0, address); 
  //radio.startListening(); 
}

void loop() {

  network.update();  // Process incoming network traffic

  while ( network.available() ) {     // If there's any data
    RF24NetworkHeader header;
    char text[40] = "";

    network.read(header, &text, sizeof(text)); // Read the data packet
    Serial.println(text); 
  }
  delay(200);

  // if (radio.available()) { 
  //   char text[40] = ""; 
  //   radio.read(&text, sizeof(text)); 
  //   Serial.println(text); 
  // } 
  // delay(200);
}