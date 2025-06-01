from serial import Serial
import serial.tools.list_ports
import time

class Arduino:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        # Automatically find the first available port if none is specified
        self.port = serial.tools.list_ports.comports()[0].device if port is None else port
        self.baudrate = baudrate 
        self.ser = None
        
        return
    
    def connect(self):
        self.ser = Serial(self.port, self.baudrate, timeout=None)
        return 

    def isconnected(self):
        if (self.ser.is_open):
            return True
        return False
    
    def close(self):
        if self.isconnected():
            self.ser.close()
        if(not self.ser.is_open):
            return True
        
        return False
    
    def readWholeMsg(self):
        msg = None
        if self.isconnected():
            msg = self.ser.readline().decode().strip()
        return msg
    
    def readMsg(self,currentPlayer):
        wholeMsg = None
        if self.isconnected():
            wholeMsg = self.ser.readline().decode().strip()
        while self.nameToId(wholeMsg) != "Node " + str(currentPlayer):
            # wait for the right player
            if self.isconnected():
                wholeMsg = self.ser.readline().decode().strip()
            continue
        # Decode the message
        move = self.decode(wholeMsg)
        # Extract the node from the message
        node = self.nameToId(wholeMsg)

        return node, move
    

    
    def nameToId(self,btnmsg):
        btnmsg = btnmsg[:6]
        return btnmsg
    
    def decode(self,msg):
        realmsg = msg[8:]
        return realmsg