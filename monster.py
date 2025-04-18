class Monster:
    def __init__(self, name, max_health, attack, shield, health_regen):
        self.name = name
        self.max_health = max_health
        self.attack = attack
        self.shield = shield
        self.health_regen = health_regen
        self.health = max_health
    
    def __str__(self):
        return f"{self.name} - Health: {self.health}/{self.max_health} - Attack: {self.attack} - Shield: {self.shield} - Health Regen: {self.health_regen}"

    # Monster receive damage
    def take_damage(self, damage):
        if self.shield > damage:
            self.shield -= damage
        elif self.shield < damage:
            damage -= self.shield
            self.health -= damage
            self.shield = 0
        else:
            self.health -= damage

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
    
    # Monster health Regeneration 
    def heal(self):
        self.health += self.health_regen
    
    def is_alive(self):
        return self.health > 0