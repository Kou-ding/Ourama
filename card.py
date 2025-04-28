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
    Card(0, "SLIFER THE SKY DRAGON", 10, 4000, 0, 0, 0, 0),
    Card(1, "OBELISK THE TORMENTOR", 10, 0, 4000, 0, 0, 0),
    Card(2, "THE WINGED GOD OF RA", 10, 0, 0, 4000, 0, 0),
    
    # Normal Cards
    # ATK Cards
    Card(3, "DARK MAGICIAN", 7, 2500, 0, 10, 0, 0),
    Card(4, "BLUE EYES WHITE DRAGON", 8, 3000, 0, 0, 0, 0),
    Card(5, "BLUE-EYES ULTIMATE DRAGON", 12, 4500, 0, 30, 0, 0),
    Card(6, "SUMMONED SKULL", 6, 2500, 0, 30, 0, 0),  
    Card(7, "FLAME SWORDSMAN", 8, 2800, 0, 0, 0, 0),
    Card(8, "KURIBOH", 1, 300, 0, 0, 0, 0),
    Card(9, "GAIA THE DRAGON CHAMPION", 7, 2600, 0, 0, 0, 0),
    Card(10, "GAIA THE FIERCE KNIGHT", 7, 2100, 0, 0, 0, 0),

    # DEF Cards
    Card(11, "RED-EYES BLACK DRAGON", 7, 0, 2400, 0, 0, 0),
    Card(12, "BIG SHIELD GARDNA", 4, 0, 2600, 0, 0, 0),
    Card(13, "DESTINY HERO - DEFENDER", 4, 0, 2700, 0, 0, 0),
    Card(14, "STONE STATUE OF THE AZTECS", 4, 0, 2000, 0, 0, 0),
    Card(15, "BLAST SPHERE", 4, 0, 1400, 0, 0, 0),
    Card(16, "GIANT SOLDIER OF STONE", 3, 0, 2000, 0, 0, 0),
    Card(17, "GRIFFORE", 4, 0, 1500, 0, 0, 0),
    Card(18, "CATAPULT TURTLE", 5, 0, 2000, 0, 0, 0),

    # HEAL Cards
    Card(19, "DARK MAGICIAN GIRL", 6, 0, 0, 2500, 0, 0),
    Card(20, "CELTIC GUARDIAN", 5, 0, 0, 1400, 0, 0),
    Card(21, "MYSTICAL ELF", 4, 0, 0, 2000, 0, 0),
    Card(22, "TIME WIZARD", 2, 0, 0, 500, 0, 0),
    Card(23, "MAGICAL ABDUCTOR", 4, 0, 0, 1700, 0, 0),
    Card(24, "SPIRIT OF THE BOOKS", 4, 0, 0, 1400, 0, 0),
    Card(25, "SPIRIT OF THE WINDS", 5, 0, 0, 1700, 0, 0),
    Card(26, "WITCH OF THE BLACK FOREST", 4, 0, 0, 1200, 0, 0),

    # Spell Cards
    # Max Health Cards
    Card(27, "MONSTER REBORN", 0, 0, 0, 0, 0, 2000),
    Card(28, "SCAPEGOAT", 0, 0, 0, 0, 0, 1000),
    Card(29, "SWORDS OF REVEALING LIGHT", 0, 0, 0, 0, 0, 1000),
    Card(30, "BLACK LUSTER RITUAL", 0, 0, 0, 0, 0, 1500),

    # Extra Energy Cards
    Card(31, "POLYMERIZATION", 0, 0, 0, 0, 10, 0),
    Card(32, "GRACEFUL CHARITY", 0, 0, 0, 0, 7, 0),
    Card(33, "GRACEFUL DICE", 0, 0, 0, 0, 5, 0),
    Card(34, "POT OF GREED", 0, 0, 0, 0, 20, 0),
]
