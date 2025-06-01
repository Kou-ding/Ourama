from card import Card
from monster import Monster
from arduino import Arduino
import time
class Player:
    def __init__(self, id, player_class, max_health, max_energy):
        self.id = id
        self.name = ""
        self.player_class = player_class
        self.max_health = max_health
        self.max_energy = max_energy
        self.health = max_health
        self.energy = max_energy
        self.shield = 0
        
    
    def setName(self, name):
        self.name = name
     
    def __str__(self):
        return f"Player {self.id} - Class: {self.player_class} - Health: {self.health}/{self.max_health} - Energy: {self.energy}/{self.max_energy} - Shield: {self.shield}" 

    def gain_shield(self, shield):
        self.shield += shield

    def heal(self, heal, Player):
        Player.health += heal
        if Player.health > Player.max_health:
            Player.health = Player.max_health

    def gain_energy(self, add_energy):
        self.energy += add_energy
    
    def increase_max_health(self, max_health):
        self.max_health += max_health
        self.health = min(self.health, self.max_health)

    def playCard(self, Card, Monster, players, arduino, current_player_id):
        if self.energy >= Card.energy:
            self.energy -= Card.energy
            if Card.attack > 0:
                Monster.take_damage(Card.attack)
                print(f"Player {self.id} played {Card.name}!")
                print(f"Player {self.id} attacked {Monster.name} for {Card.attack} damage!")
            if Card.shield > 0:
                self.gain_shield(Card.shield)
                print(f"Player {self.id} played {Card.name}!")
                print(f"Player {self.id} gained {Card.shield} shield!")
            if Card.heal > 0:
                # Check if the player is a healer
                if self.player_class != "Healer":
                    print(f"Player {self.id} is not a healer and cannot heal!")
                    # Unspend the energy
                    self.energy += Card.energy
                    return
                
                scroll = []
                for i in range(len(players)):
                    scroll.append(f"Heal {players[i].name}?") 

                print("Press left and right to scroll through players.")
                print("Press the button to select who you want to save")

                index = 0
       
                if arduino.isconnected():
                    while True:
                        time.sleep(0.5)
                        node, scroll_players = arduino.readMsg(current_player_id)
                        if scroll_players == "RIGHT":
                            index = (index + 1)% len(scroll)
                            print(scroll[index],end='\r') 
                        elif scroll_players == "LEFT":
                            index = (index - 1)% len(scroll)
                            print(scroll[index],end='\r')
                        elif scroll_players == "BTN":
                            # Clear the line before printing confirmation
                            print(" " * len(scroll[index]), end='\r')  # Clear the line
                            print(f"Player {self.id} selected {scroll[index]}!")

                            # Heal the selected player
                            self.heal(Card.heal,players[index])
                            print(f"Player {self.id} played {Card.name}!")
                            print(f"Player {self.id} healed Player {players[index].id} for {Card.heal} health!")
                            break
                
            if Card.add_energy > 0:
                self.gain_energy(Card.add_energy)
                print(f"Player {self.id} played {Card.name}!")
                print(f"Player {self.id} gained {Card.add_energy} energy!")
            if Card.add_max_health > 0:
                self.increase_max_health(Card.add_max_health)
                print(f"Player {self.id} played {Card.name}!")
                print(f"Player {self.id} increased max health by {Card.add_max_health}!")
        else:
            print(f"Player {self.id} does not have enough energy to play {Card.name}!")
            return
    def is_alive(self):
        return self.health > 0

# Child classes of the parent class Player
class Knight(Player):
    def __init__(self, id):
        super().__init__(id, player_class="Knight", max_health=8000, max_energy=10)

class Assassin(Player):
    def __init__(self, id):
        super().__init__(id, player_class="Assassin", max_health=6000, max_energy=10)

class Healer(Player):
    def __init__(self, id):
        super().__init__(id, player_class="Healer", max_health=5000, max_energy=10)

class Tank(Player):
    def __init__(self, id):
        super().__init__(id, player_class="Tank", max_health=10000, max_energy=10)
