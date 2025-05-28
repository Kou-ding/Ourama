from card import Card
from monster import Monster
class Player:
    def __init__(self, id, player_class, max_health, max_energy):
        self.id = id
        self.player_class = player_class
        self.max_health = max_health
        self.max_energy = max_energy
        self.health = max_health
        self.energy = max_energy
        self.shield = 0
    
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

    def playCard(self, Card, Monster, players, target=None):
        if self.energy < Card.energy:
            print(f"Player {self.id} does not have enough energy to play {Card.name}!")
            return

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
            if self.player_class != "Healer":
                print(f"Player {self.id} is not a healer and cannot heal!")
                self.energy += Card.energy  # Refund energy
                return
            if target and target.is_alive():
                self.heal(Card.heal, target)
                print(f"Player {self.id} played {Card.name}!")
                print(f"Player {self.id} healed Player {target.id} for {Card.heal} health!")
            else:
                print("No valid target selected for healing.")
                self.energy += Card.energy  # Refund energy
                return

        if Card.add_energy > 0:
            self.gain_energy(Card.add_energy)
            print(f"Player {self.id} played {Card.name}!")
            print(f"Player {self.id} gained {Card.add_energy} energy!")

        if Card.add_max_health > 0:
            self.increase_max_health(Card.add_max_health)
            print(f"Player {self.id} played {Card.name}!")
            print(f"Player {self.id} increased max health by {Card.add_max_health}!")
            
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
