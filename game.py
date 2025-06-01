import random
import serial
import time
import sys
from inputimeout import inputimeout, TimeoutOccurred
from arduino import Arduino
from card import cards, Card
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
        self.number_of_players = 0
        
    def initPlayersMonsters(self):
        print("Welcome to Ourama!")
        print("How many players are there?")
        # initialize the players 
        self.arduino.connect()
        if self.arduino.isconnected():
            print("Arduino is connected!")
            print("Waiting for players to connect...")
            namelist = []
            print("Press the button to add a player and toggle left or right when all players are ready")
            flag = True
            while True:
                while flag:
                    msg = self.arduino.readWholeMsg()
                    if self.arduino.decode(msg) == "LEFT" or self.arduino.decode(msg) == "RIGHT":
                        if len(namelist) != 0:
                            print("All players are ready!")
                            flag = False 
                        
                    if self.arduino.decode(msg) == "BTN" and self.arduino.nameToId(msg) not in namelist: 
                        self.number_of_players += 1
                        namelist.append(self.arduino.nameToId(msg))
                        print(f"{self.arduino.nameToId(msg)} has joined the game!")
                        time.sleep(0.5)
                        continue 
                break      
            print("End of player selection")     
            # Initialize players list with None   
            self.players = [] * self.number_of_players

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
            for i in range(self.number_of_players):     
                scroll = ["Knight  ", "Assassin", "Healer  ", "Tank    "]
                index = 0
                print("Selecting class for Player", i+1)
                time.sleep(0.5)
                print("Press left and right to scroll through classes.\nPress the button to select your class")
                print(scroll[0],end='\r')
                while True:
                    # Small delay to avoid overwhelming the Arduino
                    time.sleep(0.5)

                    # Read the message from the Arduino
                    node, move = self.arduino.readMsg(i+1)
                    flag = False
                    # Interpret the message
                    if move == "RIGHT":
                        index = (index + 1)% len(scroll)
                        print(scroll[index],end='\r') 
                    elif move == "LEFT":
                        index = (index - 1)% len(scroll)
                        print(scroll[index],end='\r')
                    elif move == "BTN":
                        selected_class = scroll[index]
                        time.sleep(0.5)  # Small delay to avoid multiple selections
                        selected_class_temp = selected_class.strip()  # Remove any extra spaces
                        print(f"Player {i+1} selected {selected_class_temp}!\n")
                        if selected_class == "Knight  ":
                            player = Knight(i+1)
                            # Set the Arduino node name
                            player.setName(node)
                            self.players.append(player)
                            flag = True
                        elif selected_class == "Assassin":
                            player = Assassin(i+1)
                            # Set the Arduino node name
                            player.setName(node)
                            self.players.append(player)
                            flag = True
                        elif selected_class == "Healer  ":
                            player = Healer(i+1)
                            # Set the Arduino node name
                            player.setName(node)
                            self.players.append(player)
                            flag = True
                        elif selected_class == "Tank    ":
                            player = Tank(i+1)
                            # Set the Arduino node name
                            player.setName(node)
                            self.players.append(player)
                            flag = True

                        # If a player has been added, break the loop
                        if flag == True:
                            break


        # Initialize 3 Monsters
        self.monsters = [None] * 3
        # name, max_health, attack, shield, health_regen, current_shield, intention[will attack?, will gain shield?], Attack probability, Shield probability
        # Scale monster stats based on number of players
        self.monsters[0] = Monster(
            name="SDOK the Charioteer",
            max_health=int(len(self.players)*5000), 
            attack=int(len(self.players)*1000/2), 
            shield=int(len(self.players)*1000/1.5), 
            health_regen=0, 
            intention=[0,0,0],
            attack_probability=50, 
            shield_probability=30) 
        self.monsters[1] = Monster(
            name="Kehagias the Wise",
            max_health=int(len(self.players)*8000), 
            attack=int(len(self.players)*2000/2),
            shield=int(len(self.players)*3000/1.5), 
            health_regen=int(len(self.players)*500/1.5), 
            intention=[0,0,0], 
            attack_probability=80, 
            shield_probability=80) 
        self.monsters[2] = Monster(
            name="Rekanos the Unhinged",
            max_health=int(len(self.players)*10000), 
            attack=int(len(self.players)*2500/2),  
            shield=int(len(self.players)*5000/1.5), 
            health_regen=int(len(self.players)*1000/1.5),  
            intention=[0,0,0], 
            attack_probability=100, 
            shield_probability=100)

        # Print the players and monsters stats
        print("\n################ Players #################") # empty line for spacing
        # View the players and monsters stats
        for i in range(len(self.players)):
            print(self.players[i].__str__())
        print("\n################ Monsters #################") # empty line for spacing
        for i in range(len(self.monsters)):
            print(self.monsters[i].__str__())
        print("\n")

        print("Players and Monsters have been initialized!\n")


    def playerTurn(self, player):
        print(f"Player {player.id}'s turn")

        # Reset player energy and shield at the start of each turn
        player.energy = player.max_energy
        player.shield = 0
        
        while not self.monsterDefeated:
            if not self.arduino.isconnected():
                self.arduino.connect()
                
            print(f"Waiting for player {player.id} with name {player.name} input...")
            
            node, move = self.arduino.readMsg(player.id)

            card_id=Card.findCard(move)

            if move=="BTN":
                print("Button pressed, ending turn.")
                break
            
            if move == "LEFT" or move == "RIGHT":
                print('Please scan a card to play.\n')  

            if len(move) > 6:
                player.playCard(cards[card_id], self.current_monster, self.players, self.arduino, player.id)
                self.checkMonsterVitals()
                self.arduino.close()
                

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
        self.current_monster.show_intention(self.players)
        
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
        print(f"You have encountered {monster.name}!\n")
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
        # Initialize players and monsters
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
