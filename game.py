import random

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


    def initPlayersMonsters(self):
        print("Welcome to Ourama!")

        print("How many players are there?")
        # Enter a valid number
        while True:
            try:
                num_players = int(input("Enter the number of players (1-4): "))
                if 1 <= num_players <= 4:
                    self.players = [None] * num_players
                    break
                else:
                    print("Invalid number of players. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("Classes:")
        print("1. Knight")
        print("2. Assassin")
        print("3. Healer")
        print("4. Tank")
 
        for i in range(num_players):
            while True:
                try:
                    choice = input(f"Player {i+1}: Choose your class (1-4): ")
                    choice = int(choice)
                    if choice == 1:
                        self.players[i] = Knight(i+1)
                        break
                    elif choice == 2:
                        self.players[i] = Assassin(i+1)
                        break
                    elif choice == 3:
                        self.players[i] = Healer(i+1)
                        break
                    elif choice == 4:
                        self.players[i] = Tank(i+1)
                        break
                    else:
                        print("Invalid choice. Please choose a valid class.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

        # Initialize 3 Monsters
        self.monsters = [None] * 3
        # name, max_health, attack, shield, health_regen, current_shield
        # Scale monster stats based on number of players
        self.monsters[0] = Monster("Rekanos", len(self.players)*5000, len(self.players)*1000/2,  len(self.players)*1000/1.5, 0, 0) 
        self.monsters[1] = Monster("Gorgon", len(self.players)*8000, len(self.players)*2000/2,  len(self.players)*3000/1.5, len(self.players)*500/1.5, 0) 
        self.monsters[2] = Monster("Golem", len(self.players)*10000, len(self.players)*2500/2,  len(self.players)*5000/1.5, len(self.players)*1000/1.5, 0)

        # View the players and monsters stats
        for i in range(len(self.players)):
            print(self.players[i].__str__())

        for i in range(len(self.monsters)):
            print(self.monsters[i].__str__())

        print("Players and Monsters have been initialized!")


    def playerTurn(self, player):
        print(f"Player {player.id}'s turn")

        # Reset player energy and shield at the start of each turn
        player.energy = player.max_energy
        player.shield = 0

        while not self.monsterDefeated:
            card_id = input("Enter the card ID to play: ")
            if card_id.strip() == "":  # End turn if input is empty
                break
            
            card_id = int(card_id)
            player.playCard(cards[card_id], self.current_monster, self.players)
            print(player.__str__())
            print(self.current_monster.__str__())
            self.checkMonsterVitals()
            

    def monsterTurn(self):
        print(f"{self.current_monster.name}'s turn")
        # Generate random number from 1 to 10
        randomizer = random.randint(1, 10)
        if self.current_monster.name == "Rekanos":
            # Even chance to attack or gain shield
            if randomizer <= 5:
                self.current_monster.gain_shield()
                print(f"{self.current_monster.name} gained shield!")
            if randomizer > 5:
                # Attack a random player
                player = random.choice(self.players)
                self.current_monster.do_damage(self.current_monster.attack, player)
                print(f"{self.current_monster.name} attacked Player {player.id}")

        elif self.current_monster.name == "Gorgon":
            # Most likely to attack
            if randomizer > 6:
                # Gain shield
                self.current_monster.gain_shield()
                print(f"{self.current_monster.name} gained shield!")
            if randomizer <= 6:
                # Attack a random player
                player = random.choice(self.players)
                self.current_monster.do_damage(self.current_monster.attack, player)
                print(f"{self.current_monster.name} attacked Player {player.id}")
            self.current_monster.heal()

        elif self.current_monster.name == "Golem":
            # Both attacks and gains shield
            if randomizer <= 5:
                # Gain shield
                self.current_monster.gain_shield()
                print(f"{self.current_monster.name} gained shield!")
            if randomizer > 3:
                # Attack a random player
                player = random.choice(self.players)
                self.current_monster.do_damage(self.current_monster.attack, player)
                print(f"{self.current_monster.name} attacked Player {player.id}")
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
        self.current_round += 1
        print(f"Round {self.current_round}")
        # Players' turn
        for player in self.players:
            # Check if the player is alive
            if not player.is_alive():
                print(f"Player {player.id} has been defeated and cannot play.")
                continue
            # Player's turn
            print(f"Player {player.id} draw 2 cards from your deck.")
            self.playerTurn(player)
            # Check if the monster is defeated
            if self.monsterDefeated:
                return
            
        # Monster's turn
        self.monsterTurn()

        for player in self.players:
            # Check if the player is alive
            if not player.is_alive():
                print(f"Player {player.id} has been defeated and cannot play.")
                continue
            

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
        # Initialize players and monsters
        self.initPlayersMonsters()

        # Experience all encounters
        for i in range(len(self.monsters)):
            self.playEncounter(self.monsters[i])
            # Prompt the players to choose 1 of 3 cards
            if i != len(self.monsters) - 1:
                print("Draw 3 new cards and choose one to add to your deck.")

        # If all encounters have played out
        print("You Win! All monsters have been defeated.")
                

# Main function to start the game
if __name__ == "__main__":
    # Initialize the game
    Ourama = Game()
    
    # Play the game
    Ourama.playGame()
