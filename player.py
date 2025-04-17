from card import Card
from monster import Monster
class Player:
    def __init__(self, name, max_health, max_energy):
        self.name = name
        self.max_health = max_health
        self.max_energy = max_energy
        self.health = max_health
        self.energy = max_energy
        self.shield = 0

    def gain_shield(self, shield):
        self.shield += shield

    def heal(self, heal):
        self.health += heal
        if self.health > self.max_health:
            self.health = self.max_health

    def gain_energy(self, add_energy):
        self.energy += add_energy
    
    def increase_max_health(self, max_health):
        self.max_health += max_health
        self.health = min(self.health, self.max_health)

    def playCard(self, Card, Monster):
        if self.energy >= Card.energy:
            self.energy -= Card.energy
            if Card.attack > 0:
                Monster.take_damage(Card.attack)
            if Card.shield > 0:
                self.gain_shield(Card.shield)
            if Card.heal > 0:
                self.heal(Card.heal)
            if Card.add_energy > 0:
                self.gain_energy(Card.add_energy)
            if Card.add_max_health > 0:
                self.increase_max_health(Card.add_max_health)
        else:
            print(f"{self.name} does not have enough energy to play {Card.name}!")
            return
    def is_alive(self):
        return self.health > 0
    def __str__(self):
        return f"{self.name} - Health: {self.health}/{self.max_health} - Energy: {self.energy}/{self.max_energy} - Shield: {self.shield}"

# Child classes of the parent class Player
class Knight(Player):
    def __init__(self):
        super().__init__(name="Knight", max_health=8000, max_energy=10)

class Assassin(Player):
    def __init__(self):
        super().__init__(name="Assassin", max_health=6000, max_energy=10)

class Healer(Player):
    def __init__(self):
        super().__init__(name="Healer", max_health=5000, max_energy=10)

class Tank(Player):
    def __init__(self):
        super().__init__(name="Tank", max_health=10000, max_energy=10)
