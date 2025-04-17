# conda activate ouenv
# Parent Player class
from card import cards
from player import Player, Knight, Assassin, Healer, Tank
from monster import Monster

class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.current_card = None
        self.rounds = 0
        self.monster = None

    def startGame(self):
        print("Welcome to Ourama!")

        player1 = Knight()
        player2 = Assassin()

        self.monster = Monster("Rekanos", 5000, 1000, 1000, 0) # name, max_health, attack, shield, health_regen

        print(f"Player 1: {player1.name} - Health: {player1.health} - Energy: {player1.energy} - Shield: {player1.shield}")
        print(f"Player 2: {player2.name} - Health: {player2.health} - Energy: {player2.energy} - Shield: {player2.shield}")
        print(f"Monster: {self.monster.name} - Health: {self.monster.health} - Attack: {self.monster.attack} - Shield: {self.monster.shield}")

        self.players.append(player1)
        self.players.append(player2)

    def playerTurn(self, player):
        print(f"{player.name}'s turn")

        while True:
            card_id = input("Enter the card ID to play: ")
            if card_id.strip() == "":  # End turn if input is empty
                break
            
            card_id = int(card_id)
            player.playCard(cards[card_id], self.monster)
            print(f"{player.name} played {cards[card_id].name}")
            print(player.__str__())
            print(self.monster.__str__())
            self.checkMonsterVitals()
            
    
    def monsterTurn(self, player):
        print(f"{self.monster.name}'s turn")
        self.monster.do_damage(self.monster.attack, player)
        print(f"{self.monster.name} attacked {player.name}")
        print(player.__str__())
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
        if not self.monster.is_alive():
            print(f"{self.monster.name} has been defeated!")
            print("Exiting the game...")
            exit()
    
    def playRound(self):
        self.rounds += 1
        print(f"Round {self.rounds}")
        # Players' turn
        for player in self.players:
            self.playerTurn(player)
            
        # Monster's turn
        for player in self.players:
            self.monsterTurn(player)
            
    
testGame=Game()
testGame.startGame()
testGame.playRound()