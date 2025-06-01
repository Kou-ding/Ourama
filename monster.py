import random

class Monster:
    def __init__(self, name, max_health, attack, shield, health_regen, intention, attack_probability, shield_probability):
        self.name = name
        self.max_health = max_health
        self.attack = attack
        self.shield = shield
        self.health_regen = health_regen
        self.health = max_health
        self.current_shield = 0
        self.intention = intention
        self.attack_probability = attack_probability
        self.shield_probability = shield_probability
    
    def __str__(self):
        return f"{self.name} - Health: {self.health}/{self.max_health} - Shield: {self.current_shield} - Health Regen: {self.health_regen}"

    # Monster receive damage
    def take_damage(self, damage):
        if self.current_shield > damage:
            self.current_shield -= damage
        elif self.current_shield < damage:
            damage -= self.current_shield
            self.health -= damage
            self.current_shield = 0
        else:
            self.health -= damage
        if self.health < 0:
            self.health = 0
    
    # Monster show intention
    def show_intention(self, players):
        # Generate random number from 1 to 10
        
        player_ids = []
        for player in players:
            if player.health > 0:
                player_ids.append(player.id)

        player_randomizer = random.randint(0, len(player_ids)-1)
        # Get the actual player ID
        player_index = player_ids[player_randomizer]  
        # Generate random number from 1 to 100
        attack_randomizer = random.randint(1, 100)
        if self.attack_probability >= attack_randomizer:
            print(f"{self.name} will attack Player {player_index} for {self.attack} damage!")
            self.intention[0] = 1
            self.intention[1] = player_index
        # Generate random number from 1 to 100
        shield_randomizer = random.randint(1, 100)
        if self.shield_probability >= shield_randomizer:
            print(f"{self.name} will shield {self.shield} damage!")
            self.intention[2] = 1
        print(f"{self.name} will heal {self.health_regen} health!")
        return

    # Monster deal damage
    def do_damage(self, damage, Player):
        if Player.shield > damage:
            Player.shield -= damage
        elif Player.shield < damage:
            damage -= Player.shield
            Player.health -= damage
            Player.shield = 0
        else:
            Player.health -= damage
        if Player.health < 0:
            Player.health = 0
    
    # Monster gain shield
    def gain_shield(self):
        self.current_shield += self.shield
        
    # Monster health Regeneration 
    def heal(self):
        if self.health + self.health_regen > self.max_health:
            self.health = self.max_health
        else:
            self.health += self.health_regen
    
    # Monster check if alive
    def is_alive(self):
        return self.health > 0