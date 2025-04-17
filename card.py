class Card:
    def __init__(self, id, name, energy, attack, shield, heal, add_energy, add_max_health):
        self.id = id
        self.name = name
        self.energy = energy
        self.attack = attack
        self.shield = shield
        self.heal = heal
        self.add_energy = add_energy
        self.add_max_health = add_max_health

# id, name, energy=stars, attack=atk, shield=def, heal, +energy, +max_health
cards = [
    # Legendary Cards
    Card(1, "SLIFER THE SKY DRAGON", 10, 4000, 0, 0, 0, 0),
    Card(2, "OBELISK THE TORMENTOR", 10, 0, 4000, 0, 0, 0),
    Card(3, "THE WINGED GOD OF RA", 10, 0, 0, 4000, 0, 0),
    
    # Normal Cards
    # ATK Cards
    Card(4, "DARK MAGICIAN", 7, 2500, 0, 10, 0, 0),
    Card(5, "BLUE EYES WHITE DRAGON", 8, 3000, 0, 0, 0, 0),
    Card(6, "BLUE-EYES ULTIMATE DRAGON", 12, 4500, 0, 30, 0, 0),
    Card(7, "SUMMONED SKULL", 6, 2500, 0, 30, 0, 0),  
    Card(8, "FLAME SWORDSMAN", 8, 2800, 0, 0, 0, 0),
    Card(9, "KURIBOH", 1, 300, 0, 0, 0, 0),
    Card(10, "GAIA THE DRAGON CHAMPION", 7, 2600, 0, 0, 0, 0),
    Card(11, "GAIA THE FIERCE KNIGHT", 7, 2100, 0, 0, 0, 0),

    # DEF Cards
    Card(12, "RED-EYES BLACK DRAGON", 7, 0, 2400, 0, 0, 0),
    Card(13, "BIG SHIELD GARDNA", 4, 0, 2600, 0, 0, 0),
    Card(14, "DESTINY HERO - DEFENDER", 4, 0, 2700, 0, 0, 0),
    Card(15, "STONE STATUE OF THE AZTECS", 4, 0, 2000, 0, 0, 0),
    Card(16, "BLAST SPHERE", 4, 0, 1400, 0, 0, 0),
    Card(17, "GIANT SOLDIER OF STONE", 3, 0, 2000, 0, 0, 0),
    Card(18, "GRIFFORE", 4, 0, 1500, 0, 0, 0),
    Card(19, "CATAPULT TURTLE", 5, 0, 2000, 0, 0, 0),

    # HEAL Cards
    Card(20, "DARK MAGICIAN GIRL", 6, 0, 0, 2500, 0, 0),
    Card(21, "CELTIC GUARDIAN", 5, 0, 0, 1400, 0, 0),
    Card(22, "MYSTICAL ELF", 4, 0, 0, 2000, 0, 0),
    Card(23, "TIME WIZARD", 2, 0, 0, 500, 0, 0),
    Card(24, "MAGICAL ABDUCTOR", 4, 0, 0, 1700, 0, 0),
    Card(25, "SPIRIT OF THE BOOKS", 4, 0, 0, 1400, 0, 0),
    Card(26, "SPIRIT OF THE WINDS", 5, 0, 0, 1700, 0, 0),
    Card(27, "WITCH OF THE BLACK FOREST", 4, 0, 0, 1200, 0, 0),

    # Spell Cards
    # Max Health Cards
    Card(28, "MONSTER REBORN", 0, 0, 0, 0, 0, 2000),
    Card(29, "SCAPEGOAT", 0, 0, 0, 0, 0, 1000),
    Card(30, "SWORDS OF REVEALING LIGHT", 0, 0, 0, 0, 0, 1000),
    Card(31, "BLACK LUSTER RITUAL", 0, 0, 0, 0, 0, 1500),

    # Extra Energy Cards
    Card(32, "POLYMERIZATION", 0, 0, 0, 0, 10, 0),
    Card(33, "GRACEFUL CHARITY", 0, 0, 0, 0, 7, 0),
    Card(34, "GRACEFUL DICE", 0, 0, 0, 0, 5, 0),
    Card(35, "POT OF GREED", 0, 0, 0, 0, 20, 0),
]
