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
    # Monster show intention
    def show_intention(self, players):
     alive_players = [p for p in players if p.is_alive()]
     if not alive_players:
         print(f"{self.name} has no valid targets.")
         self.intention = [0, 0, 0]
         return

     randomizer = random.randint(1, 10)
     target_player = random.choice(alive_players)
     
     if self.attack_probability > randomizer:
         print(f"{self.name} will attack Player {target_player.id} for {self.attack} damage!")
         self.intention[0] = 1
         self.intention[1] = target_player.id
     else:
         self.intention[0] = 0
         self.intention[1] = 0

     if self.shield_probability <= randomizer:
         print(f"{self.name} will shield {self.shield} damage!")
         self.intention[2] = 1
     else:
         self.intention[2] = 0

     print(f"{self.name} will heal {self.health_regen} health!")


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