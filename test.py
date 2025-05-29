import serial
from arduino import Arduino
arduino = Arduino()
arduino.connect()
if(arduino.isconnected()):
    while True:
        msg = arduino.clecode()
        if msg:
            print(f"Received: {msg}AAAAAAAdkfjsal")
        


