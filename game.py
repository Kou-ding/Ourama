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
       
        # Initialize 3 Monsters
        self.monsters = [None] * 3
        # name, max_health, attack, shield, health_regen, current_shield, intention[will attack?, will gain shield?], Attack probability, Shield probability
        # Scale monster stats based on number of players
        self.monsters[0] = Monster(
            name="Rekanos", 
            max_health=int(len(self.players)*5000), 
            attack=int(len(self.players)*1000/2), 
            shield=int(len(self.players)*1000/1.5), 
            health_regen=0, 
            intention=[0,0,0],
            attack_probability=5, 
            shield_probability=5) 
        self.monsters[1] = Monster(
            name="Gorgon", 
            max_health=int(len(self.players)*8000), 
            attack=int(len(self.players)*2000/2),
            shield=int(len(self.players)*3000/1.5), 
            health_regen=int(len(self.players)*500/1.5), 
            intention=[0,0,0], 
            attack_probability=6, 
            shield_probability=6) 
        self.monsters[2] = Monster(
            name="Golem", 
            max_health=int(len(self.players)*10000), 
            attack=int(len(self.players)*2500/2),  
            shield=int(len(self.players)*5000/1.5), 
            health_regen=int(len(self.players)*1000/1.5),  
            intention=[0,0,0], 
            attack_probability=4, 
            shield_probability=6)

        # View the players and monsters stats
        for i in range(len(self.players)):
            print(self.players[i].__str__())

        for i in range(len(self.monsters)):
            print(self.monsters[i].__str__())

        print("Players and Monsters have been initialized!\n")


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
            self.checkMonsterVitals()

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
        self.current_monster.show_intention(len(self.players))
        
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
                print("\nDraw 3 new cards and choose one to add to your deck.")

        # If all encounters have played out
        print("You Win! All monsters have been defeated.")
                

# Main function to start the game
if __name__ == "__main__":
    # Initialize the game
    Ourama = Game()
    
    # Play the game
    Ourama.playGame()
