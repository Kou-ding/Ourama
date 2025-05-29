import random
import serial
import time
import sys
from inputimeout import inputimeout, TimeoutOccurred
from arduino import Arduino
from card import cards
from player import Player, Knight, Assassin, Healer, Tank
from monster import Monster

class Game:
    def __init__(self):
        self.players = []
        self.current_round = 0
        self.monsters = []
        self.current_player = None
        self.current_monster = None
        self.current_card = None
        self.monsterDefeated = False
        self.arduino = Arduino()
        
        # Initialize the Arduino communicator#
        
        


    
    def initPlayersMonsters(self):
        print("Welcome to Ourama!")
        print("How many players are there?")
        # initialize the players 
        self.arduino.connect()
        if self.arduino.isconnected():
            print("Arduino is connected!")
            print("Waiting for players to connect...")
            num_players = 0
            namelist = []
            print("Press the button to add a player and toggle left or right when all players are ready")
            flag = True
            while num_players < 4 :
                while flag:
                    msg = self.arduino.readmsg()
                    if  self.arduino.decode(msg) == "LEFT" or self.arduino.decode(msg) == "RIGHT":
                        print(self.arduino.nametoid(msg))
                        if len(namelist) != 0:
                            print(msg)
                            print("All players are ready!")
                            flag = False 
                        
                    if  self.arduino.decode(msg) == "BTN" and self.arduino.nametoid(msg) not in namelist: 
                        print("Button pressed! We have a new player!")
                        num_players += 1
                        namelist.append(self.arduino.nametoid(msg))
                        print(f"Player {num_players} with name {self.arduino.nametoid(msg)} has joined the game!")
                        time.sleep(0.5)
                        continue 
                break      
            print("end of player selection")        
            self.players = [None] * num_players  # Initialize players list with None

            
            '''
            try:
                num_players = int(input("Enter the number of players (1-4): "))
                if 1 <= num_players <= 4:
                    self.players = [None] * num_players
                    break
                else:
                    print("Invalid number of players. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            '''
        print("Classes:")
        time.sleep(0.5)
        print("1. Knight")
        time.sleep(0.5)
        print("2. Assassin")
        time.sleep(0.5)
        print("3. Healer")
        time.sleep(0.5)
        print("4. Tank")
        time.sleep(1)
        
        
        if self.arduino.isconnected():
            for i in range(num_players):
                
                scroll = ["Knight  ", "Assassin", "Healer  ", "Tank    "]
                index = 0
                print("Selecting class for player", i+1)
                time.sleep(0.5)
                print("Press left and right to scroll through classes.\nPress the button to select your class")
                print(scroll[0],end='\r')
            
                while True:
                    time.sleep(0.5)  # Small delay to avoid overwhelming the Arduino
                    # Read the message from the Arduino
                    
                    wholemsg=self.arduino.readmsg()
                    msg= self.arduino.decode(wholemsg)
                    
                    if msg == "RIGHT":
                        index = (index + 1)% len(scroll)
                        print(scroll[index],end='\r') 
                    elif msg == "LEFT":
                        index = (index - 1)% len(scroll)
                        print(scroll[index],end='\r')
                    elif msg == "BTN":
                        selected_class = scroll[index]
                        time.sleep(0.5)  # Small delay to avoid multiple selections
                        print(f"Player {i+1} selected {selected_class}!")
                        if selected_class ==   "Knight  ":
                            self.players[i] = Knight(i+1)
                        elif selected_class == "Assassin":
                            self.players[i] = Assassin(i+1)
                        elif selected_class == "Healer  ":
                            self.players[i] = Healer(i+1)
                        elif selected_class == "Tank    ":
                            self.players[i] = Tank(i+1)
                          # Close the serial port after selection
                        if self.players[i] is not None:
                            print("Player initialized with class")
                            self.players[i].setnametoid(self.arduino.nametoid(wholemsg))
                            self.players[1] = Healer(2)
                            self.players[2] = Tank(3)
                            print(self.players[i].name)
                            time.sleep(2)
                        break

                                
                        
                                
                                

                            

                    
                        
                    
               
               
                # try:
                #     choice = input(f"Player {i+1}: Choose your class (1-4): ")
                #     choice = int(choice)
                #     if choice == 1:
                #         self.players[i] = Knight(i+1)
                #         break
                #     elif choice == 2:
                #         self.players[i] = Assassin(i+1)
                #         break
                #     elif choice == 3:
                #         self.players[i] = Healer(i+1)
                #         break
                #     elif choice == 4:
                #         self.players[i] = Tank(i+1)
                #         break
                #     else:
                #         print("Invalid choice. Please choose a valid class.")
                # except ValueError:
                #     print("Invalid input. Please enter a number.")
                #     continue

        # Initialize 3 Monsters
        self.monsters = [None] * 3
        # name, max_health, attack, shield, health_regen, current_shield, intention[will attack?, will gain shield?], Attack probability, Shield probability
        # Scale monster stats based on number of players
        self.monsters[0] = Monster(
            name="Rekanos", 
            max_health=int(len(self.players)*5000), 
            attack=int(len(self.players)*1000/2), 
            shield=int(len(self.players)*1000/1.5), 
            health_regen=0, 
            intention=[0,0,0],
            attack_probability=5, 
            shield_probability=5) 
        self.monsters[1] = Monster(
            name="Gorgon", 
            max_health=int(len(self.players)*8000), 
            attack=int(len(self.players)*2000/2),
            shield=int(len(self.players)*3000/1.5), 
            health_regen=int(len(self.players)*500/1.5), 
            intention=[0,0,0], 
            attack_probability=6, 
            shield_probability=6) 
        self.monsters[2] = Monster(
            name="Golem", 
            max_health=int(len(self.players)*10000), 
            attack=int(len(self.players)*2500/2),  
            shield=int(len(self.players)*5000/1.5), 
            health_regen=int(len(self.players)*1000/1.5),  
            intention=[0,0,0], 
            attack_probability=4, 
            shield_probability=6)

        # View the players and monsters stats
        for i in range(len(self.players)):
            print(self.players[i].__str__())

        for i in range(len(self.monsters)):
            print(self.monsters[i].__str__())

        print("Players and Monsters have been initialized!\n")


    def playerTurn(self, player):
        print(f"Player {player.id}'s turn")

        # Reset player energy and shield at the start of each turn
        player.energy = player.max_energy
        player.shield = 0
        
        while not self.monsterDefeated:
            if  not self.arduino.isconnected():
                self.arduino.connect()
                
            print(f"Waiting for player {player.id} with name {player.name}input...")
            
            name = player.name
            msg = self.arduino.clecode()
            if msg=="BTN":
                print("Button pressed, ending turn.")
                break
            
            if msg == "LEFT" or msg == "RIGHT":
                print('not joystick dumbfuck$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$.. Sccccannn the fking card or stop playing')  

            if len(msg) > 6:
                card_id = self.arduino.represent(msg)
                #card_id = int(card_id)
                print(msg)
                self.arduino.close()
                player.playCard(cards[card_id], self.current_monster, self.players)
                self.checkMonsterVitals()
                

    def monsterTurn(self):  
        print(f"\n{self.current_monster.name}'s turn")

        if self.current_monster.intention[0] == 1:
            # Attack a random player
            self.current_monster.do_damage(self.current_monster.attack, self.players[self.current_monster.intention[1]-1])
            print(f"{self.current_monster.name} attacked Player {self.players[self.current_monster.intention[1]-1].id} for {self.current_monster.attack} damage!")
        if self.current_monster.intention[2] == 1:
            # Gain shield
            self.current_monster.gain_shield()
            print(f"{self.current_monster.name} gained {self.current_monster.shield} shield!")
        self.current_monster.heal()
        
        # Check if any player is alive
        self.checkTeamVitals()
        

    def checkTeamVitals(self):
        endScreen = True
        for player in self.players:
            if player.is_alive():
                endScreen = False
        if endScreen:
            print("Game Over! All players have been defeated.")
            print("Exiting the game...")
            exit()
    

    def checkMonsterVitals(self):
        if not self.current_monster.is_alive():
            print(f"{self.current_monster.name} has been defeated!")
            self.monsterDefeated = True
        
    
    def playRound(self):
        # Print the current round
        self.current_round += 1
        print(f"Round {self.current_round}")

        # Print the monster's intention
        self.current_monster.show_intention(len(self.players))
        
        # Players' turn
        for player in self.players:
            # Check if the player is alive
            if not player.is_alive():
                print(f"Player {player.id} has been defeated and cannot play.")
                continue
            # Player's turn
            print(f"\nPlayer {player.id} draw 2 cards from your deck.")
            self.playerTurn(player)
            # Check if the monster is defeated
            if self.monsterDefeated:
                return
            
        # Monster's turn
        self.monsterTurn()

        for player in self.players:
            # Check if the player is alive
            if not player.is_alive():
                print(f"Player {player.id} has been slain by {self.current_monster.name}.")
                continue
        # Debugging print all players
        print("\n################ Game State #################") # empty line for spacing
        for player in self.players:
            print(player.__str__())
        # Debugging print the monster
        print(self.current_monster.__str__())
        print("#############################################\n") # empty line for spacing

    def playEncounter(self, monster):
        print(f"You have encountered {monster.name}!")
        self.current_monster = monster
        print(self.current_monster.__str__())
        while True:
            self.playRound()
            if self.monsterDefeated:
                # Reset deafeated status and current round for the next encounter
                self.monsterDefeated = False
                self.current_round = 0
                break


    def playGame(self):
        # Check if Arduino is connected
        
      
        
        self.initPlayersMonsters()

        # Experience all encounters
        for i in range(len(self.monsters)):
            self.playEncounter(self.monsters[i])
            # Prompt the players to choose 1 of 3 cards
            if i != len(self.monsters) - 1:
                print("\nDraw 3 new cards and choose one to add to your deck.")

        # If all encounters have played out
        print("You Win! All monsters have been defeated.")
                

# Main function to start the game
if __name__ == "__main__":
    # Initialize the game
    
    Ourama = Game()
    
    # Play the game
    Ourama.playGame()
