from turtle import Screen
import pygame
import sys
from player import Knight
from player import Tank
from player import Assassin
from player import Healer
from card import Card
from monster import Monster
from card import cards
SCREENWIDTH=1000
SCREENHIGHT=600
FPS =60



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager('Menu')

        self.menu = Menu(self.screen, self.gameStateManager)
        self.charactersel = CharacterSelect(self.screen, self.gameStateManager)

        # Do NOT create CharacterClass here
        self.characterclass = None  
        self.firstlevel = None
        self.states = {
            "Menu": self.menu,
            "CharacterSelect": self.charactersel,
            # Don't add CharacterClass yet
        }
    def run(self):
     while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.gameStateManager.get_state() == "Menu":
                    self.gameStateManager.set_state("CharacterSelect")

        current_state = self.gameStateManager.get_state()

        # Dynamically create CharacterClass only when switching to it
        if current_state == "CharacterClass" and self.characterclass is None:
            self.characterclass = CharacterClass(self.screen, self.gameStateManager)
            self.states["CharacterClass"] = self.characterclass
        if current_state == "FirstLevel" and self.firstlevel is None:
            self.firstlevel = FirstLevel(self.gameStateManager, self.screen)
            self.states["FirstLevel"] = self.firstlevel

        # Run current state
        self.states[current_state].run(events)

        pygame.display.update()
        self.clock.tick(FPS)

            

class CharacterSelect:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.background = pygame.image.load('background.png')  # Ensure this image exists and is loaded
        self.gameStateManager = gameStateManager
        self.player_count = self.gameStateManager.playercount # Start with 0 players
        self.font = pygame.font.SysFont(None, 60)  # Define font for rendering text
        

    def run(self, events):
     for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player_count = (self.player_count - 1) % 5
            elif event.key == pygame.K_d:
                self.player_count = (self.player_count + 1) % 5
            elif event.key == pygame.K_s:
              self.gameStateManager.set_playercount(self.player_count)
              self.gameStateManager.set_state("CharacterClass")

     self.display.blit(self.background, (0, 0))
     pygame.draw.rect(self.display, (169, 169, 169), (350, 250, 300, 100))
     text_surface = self.font.render(f'Players: {self.player_count}', True, (0, 0, 0))
     self.display.blit(text_surface, (400, 275))
     confirm_surface = self.font.render('Press SPACE to confirm', True, (255, 255, 255))
     self.display.blit(confirm_surface, (300, 200))  # Adjust position as needed
     


class Menu:
     def __init__(self,display,gameStateManager):
      self.display=display
      self.gameStateManager = gameStateManager
      self.button= pygame.image.load("start_btn.png")
      self.background = pygame.image.load('background.png')
     def run(self, events):
       self.display.blit(self.background, (0, 0))
       self.display.blit(self.button, (300,100))          # Draw button at desired position
       pygame.display.update()  




class CharacterClass:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.SysFont(None, 40)
        self.fontsmall = pygame.font.SysFont(None, 20)
        self.current_player = 1
        self.players = []
        self.max_players = self.gameStateManager.get_playercount()
        self.class_selected = False
        self.phase = 0  # 0 = selection, 1 = show stats, 2 = show message, 3 = move to next state
        self.frame_counter = 0

    def run(self, events):
        self.display.fill((0, 0, 0))  # Clear the screen

        # Phase 0: Class selection
        if self.phase == 0:
            if self.current_player <= self.max_players:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        player_obj = None
                        if event.key == pygame.K_1:
                            player_obj = Knight(self.current_player)
                        elif event.key == pygame.K_2:
                            player_obj = Assassin(self.current_player)
                        elif event.key == pygame.K_3:
                            player_obj = Healer(self.current_player)
                        elif event.key == pygame.K_4:
                            player_obj = Tank(self.current_player)

                        if player_obj:
                            self.players.append(player_obj)
                            self.current_player += 1

            if self.current_player > self.max_players:
                done_text = self.font.render("All players selected!", True, (0, 255, 0))
                self.display.blit(done_text, (250, 300))
                self.frame_counter += 1
                if self.frame_counter > 180:  # Wait 3 seconds
                    self.class_selected = True
                    self.phase = 1
                    self.frame_counter = 0
                    self.gameStateManager.players = self.players

        # Phase 1: Show stats for 10 seconds
        elif self.phase == 1:
            screen_width = SCREENWIDTH
            screen_height = SCREENHIGHT
            section_width = screen_width // 2
            section_height = screen_height // 2

            for i, player in enumerate(self.players):
                if i == 0:
                    x, y = 20, 20
                elif i == 1:
                    x, y = section_width + 20, 20
                elif i == 2:
                    x, y = 20, section_height + 20
                elif i == 3:
                    x, y = section_width + 20, section_height + 20

                text_surface = self.font.render(player.__class__.__name__, True, (255, 255, 255))
                self.display.blit(text_surface, (x, y))
                energy_surface = self.fontsmall.render(f"Max Energy: {player.max_energy}", True, (255, 255, 255))
                self.display.blit(energy_surface, (x, y + 30))
                health_surface = self.fontsmall.render(f"Max Health: {player.max_health}", True, (255, 255, 255))
                self.display.blit(health_surface, (x, y + 50))

                class_color = (100, 100, 100)
                if player.player_class == "Knight":
                    class_color = (255, 0, 0)
                elif player.player_class == "Tank":
                    class_color = (0, 255, 0)
                elif player.player_class == "Healer":
                    class_color = (0, 0, 255)
                pygame.draw.rect(self.display, class_color, (x, y + 80, 100, 20))

            self.frame_counter += 1
            if self.frame_counter > 600:  # 10 seconds
                self.frame_counter = 0
                self.phase = 2

        # Phase 2: Show black screen + message
        elif self.phase == 2:
            self.display.fill((0, 0, 0))
            message = self.font.render("The journey of our Heroes starts", True, (255, 87, 51))
            self.display.blit(message, (200, 280))
            self.frame_counter += 1
            if self.frame_counter > 300:  # 5 seconds
                self.phase = 3

        # Phase 3: Transition to FirstLevel
        elif self.phase == 3:
            self.gameStateManager.set_state("FirstLevel")
        pygame.display.update()  # Update the display


class Level:
    def __init__(self, gameStateManager, display):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.SysFont(None, 40)
        self.fontsmall = pygame.font.SysFont(None, 30)
        self.players = self.gameStateManager.players
        self.background = pygame.image.load("swamptower.jpg")  # picture "endiktikh"
        self.round =0
        self.current_player_index=0 #index to know who the f is playing
        self.battle_over=False #Boolean for defeat screen
        self.card_input = ""

        # Initialize monster (first boss)
        player_count = len(self.players)
        self.boss = Monster(
            name="Rekanos", 
            max_health=int(player_count * 5000), 
            attack=int(player_count * 1000 / 2), 
            shield=int(player_count * 1000 / 1.5), 
            health_regen=0, 
            intention=[0, 0, 0],
            attack_probability=5, 
            shield_probability=5
        )
        self.boss_image = pygame.image.load("firstboss.jpg").convert_alpha()
        self.boss_rect = self.boss_image.get_rect(topleft=(700,200))  
        self.bossDefeated=False

       # ##initialize the player
       # for player in self.players:
       #     player.energy=player.max_energy
       #     player.shield=0
       # #intetions of monster for the players
        self.boss.show_intention(len(self.players))

    #colour for each class
    def get_class_color(self, player):
     if player.player_class == "Knight":
        return (255, 0, 0)  # Red
     elif player.player_class == "Tank":
        return (0, 255, 0)  # Green
     elif player.player_class == "Healer":
        return (0, 0, 255)  # Blue
     elif player.player_class == "Assassin":
        return (255, 255, 0)  # Yellow
     return (100, 100, 100)  # Default gray

    #basically victory function
    def  check_monster_vitals(self):
        if not self.boss.is_alive():
            print(f"The monster has been defeated")
            self.bossDefeated=True
            self.battle_over=True

    def check_team_vitals(self):
       endScreen = True
       for player in self.players:
           if player.is_alive():
               endScreen = False
       if endScreen:
           print("Game Over! All players have been defeated.")
           print("Exiting the game...")
           exit()
    
    #for monster
    def draw_health_bar(self):
        bar_width=200
        bar_height=20
        health_ratio =self.boss.health/self.boss.max_health #ousiastika poso posostiaia peftei to hp
        pygame.draw.rect(self.display,(255,0,0),(self.boss_rect.x,self.boss_rect.y-30,bar_width,bar_height))
        pygame.draw.rect(self.display, (0, 255, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width * health_ratio, bar_height))
        boss_name=self.font.render(self.boss.name,True,(255,255,255))
        self.display.blit(boss_name,(self.boss_rect.x,self.boss_rect.y-55))


    #for players
    def draw_player_bars(self, player, rect):
     full_bar_width = 100
     health_bar_height = 10
     energy_bar_height = 5

     # Health bar (Red background, Green foreground)
     health_ratio = player.health / player.max_health
     pygame.draw.rect(self.display, (255, 0, 0), (rect.x, rect.y - 25, full_bar_width, health_bar_height))
     pygame.draw.rect(self.display, (0, 255, 0), (rect.x, rect.y - 25, full_bar_width * health_ratio, health_bar_height))

     # Energy bar (Gray background, Blue foreground — thinner)
     energy_ratio = player.energy / player.max_energy
     pygame.draw.rect(self.display, (50, 50, 50), (rect.x, rect.y - 12, full_bar_width, energy_bar_height))
     pygame.draw.rect(self.display, (0, 0, 255), (rect.x, rect.y - 12, full_bar_width * energy_ratio, energy_bar_height))

     # Optional: Draw player name/ID above bars
     player_name = self.font.render(f"P{player.id}", True, (255, 255, 255))
     self.display.blit(player_name, (rect.x, rect.y - 45))

    #draw players and health/energy bars
    def draw_players(self):
     start_x = 50
     start_y = 500
     box_width = 100
     box_height = 40
     gap = 120
 
     for i, player in enumerate(self.players):
        x = start_x + i * gap
        y = start_y
        rect = pygame.Rect(x, y, box_width, box_height)

        # Draw health and energy bars above the box
        self.draw_player_bars(player, rect)

        # Draw player class box
        color = self.get_class_color(player)
        pygame.draw.rect(self.display, color, rect)

        # Draw class name
        name_surface = self.fontsmall.render(player.player_class, True, (255, 255, 255))
        self.display.blit(name_surface, (x + 5, y + 10))


 
    #Maybe it needs modifications {San to PlayerTurn}
    def handle_player_turn(self, player, events):
     for event in events:
        if event.type == pygame.KEYDOWN:
           #edw einai ligo kati pou den mou paei kala
            if event.unicode.isdigit():
                self.card_input += event.unicode
                print(f"Card ID input: {self.card_input}")
            
            # If Enter is pressed, try to parse and play the card
            elif event.key == pygame.K_RETURN:
                if self.card_input:
                    try:
                        card_id = int(self.card_input)
                        if 0 <= card_id < len(cards):
                            player.playCard(cards[card_id], self.boss, self.players)
                            print(f"Player {player.id} played card: {cards[card_id].name}")
                        else:
                            print(f"Invalid card ID: {card_id}")
                    except ValueError:
                        print("Invalid input")
                    finally:
                        self.card_input = ""  # Reset after attempting to play
                        
            # Optional: allow backspace to delete last digit
            elif event.key == pygame.K_BACKSPACE:
                self.card_input = self.card_input[:-1]


    #Checks if the turn of the player is finished to jump to the next
    def turn_finished(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
        return False
    

    #San to monster turn
    def monster_turn(self):
        #attack
        if self.boss.intention[0] == 1:
            target = self.players[self.boss.intention[1] - 1]
            #checks if the target is alive to attack
            if target.is_alive():
                self.boss.do_damage(self.boss.attack, target)
                print(f"{self.boss.name} attacked Player {target.id} for {self.boss.attack} damage!")
        #shield        
        if self.boss.intention[2] == 1:
            self.boss.gain_shield()
            print(f"{self.boss.name} gained {self.boss.shield} shield!")
        #heal
        self.boss.heal()

    def run(self,events):
        #checks if the battle is over or not
      if self.battle_over:
            return
     
      self.players = self.gameStateManager.players
      self.display.blit(self.background, (0, 0))
      self.display.blit(self.boss_image, self.boss_rect) 
      #Setting up the players and the healthbars
      self.draw_health_bar()
      self.draw_players() 

      # Check win/lose condition
      self.check_monster_vitals()
      self.check_team_vitals()
      
      if self.bossDefeated or self.battle_over:
            return

        # Run current player’s turn logic
      current_player = self.players[self.current_player_index]
      if current_player.is_alive():
            self.handle_player_turn(current_player, events)

        # Advance to next player or boss turn
      if self.turn_finished(events):
            self.current_player_index += 1
            #checks if all the players have played
            if self.current_player_index >= len(self.players):
                #monster turn
                self.monster_turn()
                self.current_player_index = 0 #resets index to start the round all over again
                self.round += 1  #round +1
                self.boss.show_intention(len(self.players)) #sets boss's new intention?
                for player in self.players:   
                    player.energy = player.max_energy  #energy reset
                    player.shield = 0                  #shield reset?Does yigioh work like that?



class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        self.players = []
        self.playercount = 0  # Initialize properly

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

    def get_playercount(self):
        return self.playercount

    def set_playercount(self, playercount):
        self.playercount = playercount
   

if __name__ == '__main__':           
  game = Game()
  game.run()
