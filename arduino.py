from serial import Serial
import serial.tools.list_ports
#from player import Player  # Assuming Player class is defined in player.py
import time

class Arduino:

    
    def __init__(self, port=None, baudrate=9600):
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
    
    def readmsg(self):
        msg = None
        if self.isconnected():
            msg = self.ser.readline().decode().strip()
        return msg
    '''
    not needed yet
    
    def naming(self,id):
        if self.readmsg() is not None:
            msg = self.readmsg()
            Player.players[id].nametoid(msg)
        return Player.players[id].name 
    '''
    def nametoid(self,btnmsg):
        btnmsg = btnmsg[:8]
        return btnmsg
    
    def decode(self,msg):
        realmsg = msg[10:]
        return realmsg

    def clecode(self):
        msg = self.readmsg()
        msg = self.decode(msg)
        return msg
    
    # def countdown(self,t,namelist=[]):
        
    #     while t:
    #         msg= self.readmsg()
    #         if msg == "BTN" and Player.nametoid(msg) not in namelist:
    #             break
    #         secs = divmod(t,60)
    #         timer = '{:02d}'.format(secs[1])
    #         print(timer, end="\r")
    #         time.sleep(1)
    #         t -=1
    #     return t
    
    def represent(self,msg):
        if msg == "3b6dcd48":
            return 22
        return 1
        
'''       
if __name__ == '__main__':  
    arduino = Arduino()
    arduino.connect()
    countdown_time = 10  # Set countdown time in seconds
    print("Starting countdown...for {countdown_time}")
    arduino.countdown(countdown_time)
    print("Countdown finished!")
    
    

    if arduino.isconnected():
        print("Connected to Arduino and waiting for messages...")
        while True:
            msg = arduino.clecode()
            if msg is not None:
                print(f"Received: {msg}")
                if msg =="BTN":
                    print("Button pressed!")
                    break  # Exit the loop on button press
    else:
        print("Failed to connect to Arduino")
    pl = Player()
    players=[]
    countdown = 10
    maxplayers= 0
    scroll = ["Knight", "Assasin", "Healer", "Tank"]
    if arduino.isconnected():
        while countdown ==0 or maxplayers > 4:
            
            #Player.name = Player.nametoid(arduino.readmsg())
            msg = arduino.clecode()
            if msg == "BTN":
                time.sleep(0.5)
                print("Button pressed!We have a new player! Select your class dumbfuck!")
                print("The classes are :Knight, Assasin, Healer, Tank")
                maxplayers = maxplayers + 1
                players.append(Player())
                while True:
                    print("Waiting for Player {maxplayers} with name {Player.nametoid(arduino.readmsg())}...")
                    print("Select a class Player {maxplayers} : ")
                    if arduino.isconnected():
                        msg = arduino.clecode()
                        if msg in scroll:
                           
                            Player.name = Player.nametoid(arduino.readmsg())
                            Player.id = maxplayers
                            if msg == "LEFT":
                                
                                
                            elif msg == "RIGHT":
                                
                            elif msg == "BTN":
                                players[maxplayers-1] = Player.Healer(Player.id)
                            break
                        else:
                            print("Invalid class selection. Please try again.")                    
                                        
        for i in range(4):
            Player.id = i + 1
            players[i] = Player.Knight(Player.id)
            
    arduino.close()
    if arduino.close():
        print("Connection closed")
        '''
        
        