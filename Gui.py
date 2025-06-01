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
        self.secondlevel=None
        self.thirdlevel=None
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
        if current_state == "SecondLevel" and self.secondlevel is None:    
            self.secondlevel = SecondLevel(self.screen,self.gameStateManager)
            self.states["SecondLevel"] = self.secondlevel
        if current_state == "ThirdLevel" and self.thirdlevel is None:    
            self.thirdlevel= ThirdLevel(self.screen,self.gameStateManager)
            self.states["ThirdLevel"] = self.thirdlevel



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
        self.KnightIcon=pygame.image.load("Knight.png")
        self.TankIcon=pygame.image.load("Tank.png")
        self.HealerIcon=pygame.image.load("Healer.png")
        self.AssassinIcon=pygame.image.load("Assasin.png")
        self.class_icons = {
            "Knight": self.KnightIcon,
            "Tank": self.TankIcon,
            "Healer": self.HealerIcon,
            "Assassin": self.AssassinIcon
              }

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
                 origin_x, origin_y = 0, 0
             elif i == 1:
                 origin_x, origin_y = section_width, 0
             elif i == 2:
                 origin_x, origin_y = 0, section_height
             elif i == 3:
                 origin_x, origin_y = section_width, section_height

             center_x = origin_x + section_width // 2
             center_y = origin_y + section_height // 2

             # Draw class icon
             icon = self.class_icons.get(player.player_class)
             if icon:
                 icon_rect = icon.get_rect(center=(center_x, center_y - 40))  # icon slightly above center
                 self.display.blit(icon, icon_rect)

             # Draw class name
             text_surface = self.font.render(player.__class__.__name__, True, (255, 255, 255))
             text_rect = text_surface.get_rect(center=(center_x, center_y + 40))
             self.display.blit(text_surface, text_rect)

             # Draw max energy
             energy_surface = self.fontsmall.render(f"Max Energy: {player.max_energy}", True, (255, 255, 255))
             energy_rect = energy_surface.get_rect(center=(center_x, center_y + 65))
             self.display.blit(energy_surface, energy_rect)

             # Draw max health
             health_surface = self.fontsmall.render(f"Max Health: {player.max_health}", True, (255, 255, 255))
             health_rect = health_surface.get_rect(center=(center_x, center_y + 85))
             self.display.blit(health_surface, health_rect)

             # Class color bar
             class_color = (100, 100, 100)
             if player.player_class == "Knight":
                 class_color = (255, 0, 0)
             elif player.player_class == "Tank":
                 class_color = (0, 255, 0)
             elif player.player_class == "Healer":
                 class_color = (0, 0, 255)
             elif player.player_class == "Assassin":
                 class_color = (255, 255, 0)

             pygame.draw.rect(self.display, class_color, (center_x - 50, center_y + 105, 100, 10))

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


class FirstLevel:
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
        self.selected_card = None
        self.pending_heal_card = None
        self.healer_player = None
        self.victory_screen = False
        self.defeat_screen = False
        self.screen_timer = 0 
        self.defeatscreen=pygame.image.load("defeat.png")
        self.victoryscreen=pygame.image.load("victory.jpg")
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
        self.healthbar=pygame.image.load("healthbar.png")
        self.energyicon=pygame.image.load("energyicon.png")
        self.healingicon=pygame.image.load("healingicon.png").convert_alpha()
      # self.armouricon=pygame.image.load("armouricon.png")
        self.swordicon=pygame.image.load("swordicon.png").convert_alpha()
        self.shieldicon=pygame.image.load("shieldicon.png").convert_alpha()
        self.KnightIcon=pygame.image.load("Knight.png")
        self.TankIcon=pygame.image.load("Tank.png")
        self.HealerIcon=pygame.image.load("Healer.png")
        self.AssassinIcon=pygame.image.load("Assasin.png")
        self.class_icons = {
            "Knight": self.KnightIcon,
            "Tank": self.TankIcon,
            "Healer": self.HealerIcon,
            "Assassin": self.AssassinIcon
              }
        self.heal_target_index = 0


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
        self.boss.show_intention(self.players)
       # ##initialize the player
       # for player in self.players:
       #     player.energy=player.max_energy
       #     player.shield=0
       # #intetions of monster for the players

     #Check;s if monster is defeated
    def check_monster_vitals(self):
     if not self.boss.is_alive() and not self.victory_screen:
        print("The monster has been defeated")
        self.battle_over = True
        self.victory_screen = True
        self.screen_timer = pygame.time.get_ticks()  # Start timer

    def check_team_vitals(self):
     if all(not player.is_alive() for player in self.players) and not self.defeat_screen:
        print("All players have been defeated.")
        self.battle_over = True
        self.defeat_screen = True
        self.screen_timer = pygame.time.get_ticks()  # Start timer

     #victory screen
    def draw_victory_screen(self):
     self.display.blit(self.victoryscreen,(0,0))
     text = self.font.render("Draw 3 cards but only choose 1", True, (255, 255, 255))
     self.display.blit(text, (250, 300))

     #defeat screen
    def draw_defeat_screen(self):
     self.display.fill((0,0,0))
     self.display.blit(self.defeatscreen, (100,150))   
     
    #for monster
    def draw_health_bar(self):
     bar_width = 200
     bar_height = 20
     health_ratio = self.boss.health / self.boss.max_health
 
     # Health bar
     pygame.draw.rect(self.display, (255, 0, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width, bar_height))
     pygame.draw.rect(self.display, (0, 255, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width * health_ratio, bar_height))
 
     # Boss name
     boss_name = self.font.render(self.boss.name, True, (255, 255, 255))
     self.display.blit(boss_name, (self.boss_rect.x, self.boss_rect.y - 55))
 
     # Intention icons [attack, shield, heal]{enumerate the intentions (making a vocabulary)}
     icon_map = {0: self.swordicon, 2: self.shieldicon, 3: self.healingicon}
     icon_size = 40
     icon_spacing = 5
 
     # Count how many active intentions to center them
     active_intentions = [i for i in (0, 2, 3) if i < len(self.boss.intention) and self.boss.intention[i] == 1]
     active_count = len(active_intentions)
     start_x = self.boss_rect.x + (self.boss_rect.width // 2) - ((icon_size + icon_spacing) * active_count - icon_spacing) // 2
     icon_y = self.boss_rect.y - 80
 
     # Draw each active icon
     icon_x = start_x
     for i in active_intentions:
         icon = pygame.transform.scale(icon_map[i], (icon_size, icon_size))
         self.display.blit(icon, (icon_x, icon_y))
         icon_x += icon_size + icon_spacing


    #for players
    def draw_player_bars(self, player, rect):
     full_bar_width = 100
     health_bar_height = 10
     energy_bar_height = 5
    
     healthbar_bg = pygame.transform.scale(self.healthbar, (120, 14))  # Adjust if needed
     healthbar_pos = (rect.x - 20, rect.y - 28)  # Position it slightly to the left of the player sprite
     self.display.blit(healthbar_bg, healthbar_pos)
 
     # Calculate filled health portion
     health_ratio = player.health / player.max_health
     fill_width = int(102* health_ratio)  # The fillable part of the bar inside (approximate)
     fill_height = 5
     fill_x = healthbar_pos[0] + 16  # Start of the green fill inside the image
     fill_y = healthbar_pos[1] + 5  # Vertically centered

    # Draw the green fill bar (actual health)
     pygame.draw.rect(self.display, (0, 255, 0), (fill_x, fill_y, fill_width, fill_height))
     
     # Energy bar (Gray background, Blue foreground — thinner)
     energy_ratio = player.energy / player.max_energy
     pygame.draw.rect(self.display, (50, 50, 50), (rect.x, rect.y - 12, full_bar_width, energy_bar_height))
     pygame.draw.rect(self.display, (0, 0, 255), (rect.x, rect.y - 12, full_bar_width * energy_ratio, energy_bar_height))
  
     icon_size = 12  # Resize icon to fit nicely
     resized_icon = pygame.transform.scale(self.energyicon, (icon_size, icon_size))
     icon_x = rect.x - icon_size - 3  # 5 pixels gap from the bar
     icon_y = rect.y - 12  # Align with energy bar
     self.display.blit(resized_icon, (icon_x, icon_y))


     # Optional: Draw player name/ID above bars
     player_name = self.font.render(f"P{player.id}", True, (255, 255, 255))
     self.display.blit(player_name, (rect.x, rect.y - 45))
     # Draw arrow if healer is selecting a target
     
    def get_class_icon(self, player):
     if player.player_class == "Knight":
        return self.KnightIcon
     elif player.player_class == "Tank":
        return self.TankIcon
     elif player.player_class == "Healer":
        return self.HealerIcon
     elif player.player_class == "Assassin":
         return self.AssassinIcon
     else:
        return pygame.Surface((100, 40))  # fallback blank surface if unknown class

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
        icon = self.get_class_icon(player)
        icon_resized = pygame.transform.scale(icon, (box_width, box_height))
        self.display.blit(icon_resized, (x, y))

       
        if self.pending_heal_card and self.healer_player is not None and self.heal_target_index == i:
         arrow_rect = self.arrow_image.get_rect(center=(x + box_width // 2, y - 60))
         self.display.blit(self.arrow_image, arrow_rect)



      #Maybe it needs modifications {San to PlayerTurn}
    def handle_player_turn(self, player, events):
    # 1. Healing target selection mode: handle arrow keys, confirm, cancel
     if self.pending_heal_card and self.healer_player == player:
         for event in events:
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_a:
                     self.heal_target_index = (self.heal_target_index - 1) % len(self.players)
                     while not self.players[self.heal_target_index].is_alive():
                         self.heal_target_index = (self.heal_target_index - 1) % len(self.players)

                 elif event.key == pygame.K_d:
                     self.heal_target_index = (self.heal_target_index + 1) % len(self.players)
                     while not self.players[self.heal_target_index].is_alive():
                         self.heal_target_index = (self.heal_target_index + 1) % len(self.players)

                 elif event.key == pygame.K_RETURN:
                     target_player = self.players[self.heal_target_index]
                     if target_player.is_alive():
                         self.healer_player.playCard(self.pending_heal_card, self.boss, self.players, target=target_player)
                         self.pending_heal_card = None
                         self.healer_player = None
                         print("Healing complete.")
                     else:
                         print("Selected player is not alive!")

                 elif event.key == pygame.K_ESCAPE:
                     print("Healing cancelled.")
                     self.pending_heal_card = None
                     self.healer_player = None
         return  # Skip the rest of the turn while healing target selecting

     # 2. Normal card input mode
     for event in events:
         if event.type == pygame.KEYDOWN:
             if event.unicode.isdigit():
                 self.card_input += event.unicode
                 print(f"Card ID input: {self.card_input}")

             elif event.key == pygame.K_BACKSPACE:
                 self.card_input = self.card_input[:-1]

             elif event.key == pygame.K_RETURN:
                 if self.card_input:
                     try:
                         card_id = int(self.card_input)
                         if 0 <= card_id < len(cards):
                             selected_card = cards[card_id]
                             if player.energy >= selected_card.energy:
                                 if selected_card.heal > 0 and player.player_class == "Healer":
                                     # Enter healing mode - set pending heal card and healer player
                                     self.pending_heal_card = selected_card
                                     self.healer_player = player
                                     self.heal_target_index = 0  # reset heal target index
                                     print(f"Selected healing card: {selected_card.name}. Use A/D to choose target, Enter to confirm.")
                                 else:
                                     player.playCard(selected_card, self.boss, self.players)
                                     print(f"Player {player.id} played card: {selected_card.name}")
                             else:
                                 print("Not enough energy!")
                         else:
                             print(f"Invalid card ID: {card_id}")
                     except ValueError:
                         print("Invalid input")
                     finally:
                         self.card_input = ""


    #Checks if the turn of the player is finished to jump to the next
    def turn_finished(self, events):
     for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            print("Player Round ended")
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
         
      if self.victory_screen:
         self.draw_victory_screen()
         if pygame.time.get_ticks() - self.screen_timer > 3000:  # 3 seconds delay
            self.gameStateManager.players = self.players
            self.gameStateManager.set_state("SecondLevel")  # You must define this
            
      if self.defeat_screen:
         self.draw_defeat_screen()
        
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
                self.boss.show_intention(self.players) #sets boss's new intention?
                for player in self.players:   
                    player.energy = player.max_energy  #energy reset
                    player.shield = 0                  #shield reset?Does yigioh work like that?
            pygame.display.update()                



class SecondLevel: 
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.SysFont(None, 40)
        self.fontsmall = pygame.font.SysFont(None, 30)
        self.players = self.gameStateManager.players
        self.background = pygame.image.load("lonelybridge.jpg")  # picture "endiktikh"
        self.round =0
        self.current_player_index=0 #index to know who the f is playing
        self.battle_over=False #Boolean for defeat screen
        self.card_input = ""
        self.selected_card = None
        self.pending_heal_card = None
        self.healer_player = None
        self.victory_screen = False
        self.defeat_screen = False
        self.screen_timer = 0 
        self.defeatscreen=pygame.image.load("defeat.png")
        self.victoryscreen=pygame.image.load("victory.jpg")
        self.phase = True
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
        self.heal_target_index = 0
        self.defeatscreen=pygame.image.load("defeat.png")
        self.victoryscreen=pygame.image.load("victory.jpg")
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
        self.healthbar=pygame.image.load("healthbar.png")
        self.energyicon=pygame.image.load("energyicon.png")
        self.healingicon=pygame.image.load("healingicon.png")
      # self.armouricon=pygame.image.load("armouricon.png")
        self.swordicon=pygame.image.load("swordicon.png")
        self.shieldicon=pygame.image.load("shieldicon.png")
        self.KnightIcon=pygame.image.load("Knight.png")
        self.TankIcon=pygame.image.load("Tank.png")
        self.HealerIcon=pygame.image.load("Healer.png")
        self.AssassinIcon=pygame.image.load("Assasin.png")
        self.class_icons = {
            "Knight": self.KnightIcon,
            "Tank": self.TankIcon,
            "Healer": self.HealerIcon,
            "Assassin": self.AssassinIcon
              }
       
        player_count = len(self.players)
        self.boss = Monster(
            name="Gorgon", 
            max_health=int(len(self.players)*8000), 
            attack=int(len(self.players)*2000/2),
            shield=int(len(self.players)*3000/1.5), 
            health_regen=int(len(self.players)*500/1.5), 
            intention=[0,0,0], 
            attack_probability=6, 
            shield_probability=6)
        self.boss_image = pygame.image.load("secondboss.png").convert_alpha()
        self.boss_rect = self.boss_image.get_rect(topleft=(700,200))  
        self.bossDefeated=False
        self.boss.show_intention(self.players)

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

     #Check;s if monster is defeated
    def check_monster_vitals(self):
     if not self.boss.is_alive() and not self.victory_screen:
        print("The monster has been defeated")
        self.battle_over = True
        self.victory_screen = True
        self.screen_timer = pygame.time.get_ticks()  # Start timer    




    def check_team_vitals(self):
      if all(not player.is_alive() for player in self.players) and not self.defeat_screen:
        print("All players have been defeated.")
        self.battle_over = True
        self.defeat_screen = True
        self.screen_timer = pygame.time.get_ticks()  # Start timer

    def draw_victory_screen(self):
     self.display.blit(self.victoryscreen,(0,0))
     text = self.font.render("Draw 3 cards but only choose 1", True, (255, 255, 255))
     self.display.blit(text, (250, 300))

     #defeat screen
    def draw_defeat_screen(self):
     self.display.fill((0,0,0))
     self.display.blit(self.defeatscreen, (100,150))   
     
   #for monster
    def draw_health_bar(self):
     bar_width = 200
     bar_height = 20
     health_ratio = self.boss.health / self.boss.max_health
 
     # Health bar
     pygame.draw.rect(self.display, (255, 0, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width, bar_height))
     pygame.draw.rect(self.display, (0, 255, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width * health_ratio, bar_height))
 
     # Boss name
     boss_name = self.font.render(self.boss.name, True, (255, 255, 255))
     self.display.blit(boss_name, (self.boss_rect.x, self.boss_rect.y - 55))
 
     # Intention icons [attack, shield, heal]{enumerate the intentions (making a vocabulary)}
     icon_map = {0: self.swordicon, 2: self.shieldicon, 3: self.healingicon}
     icon_size = 40
     icon_spacing = 5
 
     # Count how many active intentions to center them
     active_intentions = [i for i in (0, 2, 3) if i < len(self.boss.intention) and self.boss.intention[i] == 1]
     active_count = len(active_intentions)
     start_x = self.boss_rect.x + (self.boss_rect.width // 2) - ((icon_size + icon_spacing) * active_count - icon_spacing) // 2
     icon_y = self.boss_rect.y - 80
 
     # Draw each active icon
     icon_x = start_x
     for i in active_intentions:
         icon = pygame.transform.scale(icon_map[i], (icon_size, icon_size))
         self.display.blit(icon, (icon_x, icon_y))
         icon_x += icon_size + icon_spacing


     #for players
    def draw_player_bars(self, player, rect):
     full_bar_width = 100
     health_bar_height = 10
     energy_bar_height = 5
    
     healthbar_bg = pygame.transform.scale(self.healthbar, (120, 14))  # Adjust if needed
     healthbar_pos = (rect.x - 20, rect.y - 28)  # Position it slightly to the left of the player sprite
     self.display.blit(healthbar_bg, healthbar_pos)
 
     # Calculate filled health portion
     health_ratio = player.health / player.max_health
     fill_width = int(102* health_ratio)  # The fillable part of the bar inside (approximate)
     fill_height = 5
     fill_x = healthbar_pos[0] + 16  # Start of the green fill inside the image
     fill_y = healthbar_pos[1] + 5  # Vertically centered

    # Draw the green fill bar (actual health)
     pygame.draw.rect(self.display, (0, 255, 0), (fill_x, fill_y, fill_width, fill_height))
     
     # Energy bar (Gray background, Blue foreground — thinner)
     energy_ratio = player.energy / player.max_energy
     pygame.draw.rect(self.display, (50, 50, 50), (rect.x, rect.y - 12, full_bar_width, energy_bar_height))
     pygame.draw.rect(self.display, (0, 0, 255), (rect.x, rect.y - 12, full_bar_width * energy_ratio, energy_bar_height))
  
     icon_size = 12  # Resize icon to fit nicely
     resized_icon = pygame.transform.scale(self.energyicon, (icon_size, icon_size))
     icon_x = rect.x - icon_size - 3  # 5 pixels gap from the bar
     icon_y = rect.y - 12  # Align with energy bar
     self.display.blit(resized_icon, (icon_x, icon_y))


     # Optional: Draw player name/ID above bars
     player_name = self.font.render(f"P{player.id}", True, (255, 255, 255))
     self.display.blit(player_name, (rect.x, rect.y - 45))
     # Draw arrow if healer is selecting a target
     
    def get_class_icon(self, player):
     if player.player_class == "Knight":
        return self.KnightIcon
     elif player.player_class == "Tank":
        return self.TankIcon
     elif player.player_class == "Healer":
        return self.HealerIcon
     elif player.player_class == "Assassin":
         return self.AssassinIcon
     else:
        return pygame.Surface((100, 40))  # fallback blank surface if unknown class

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
        icon = self.get_class_icon(player)
        icon_resized = pygame.transform.scale(icon, (box_width, box_height))
        self.display.blit(icon_resized, (x, y))

       
        if self.pending_heal_card and self.healer_player is not None and self.heal_target_index == i:
         arrow_rect = self.arrow_image.get_rect(center=(x + box_width // 2, y - 60))
         self.display.blit(self.arrow_image, arrow_rect)


    #Maybe it needs modifications {San to PlayerTurn}
    def handle_player_turn(self, player, events):
    # 1. Healing target selection mode: handle arrow keys, confirm, cancel
     if self.pending_heal_card and self.healer_player == player:
         for event in events:
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_a:
                     self.heal_target_index = (self.heal_target_index - 1) % len(self.players)
                     while not self.players[self.heal_target_index].is_alive():
                         self.heal_target_index = (self.heal_target_index - 1) % len(self.players)

                 elif event.key == pygame.K_d:
                     self.heal_target_index = (self.heal_target_index + 1) % len(self.players)
                     while not self.players[self.heal_target_index].is_alive():
                         self.heal_target_index = (self.heal_target_index + 1) % len(self.players)

                 elif event.key == pygame.K_RETURN:
                     target_player = self.players[self.heal_target_index]
                     if target_player.is_alive():
                         self.healer_player.playCard(self.pending_heal_card, self.boss, self.players, target=target_player)
                         self.pending_heal_card = None
                         self.healer_player = None
                         print("Healing complete.")
                     else:
                         print("Selected player is not alive!")

                 elif event.key == pygame.K_ESCAPE:
                     print("Healing cancelled.")
                     self.pending_heal_card = None
                     self.healer_player = None
         return  # Skip the rest of the turn while healing target selecting

     # 2. Normal card input mode
     for event in events:
         if event.type == pygame.KEYDOWN:
             if event.unicode.isdigit():
                 self.card_input += event.unicode
                 print(f"Card ID input: {self.card_input}")

             elif event.key == pygame.K_BACKSPACE:
                 self.card_input = self.card_input[:-1]

             elif event.key == pygame.K_RETURN:
                 if self.card_input:
                     try:
                         card_id = int(self.card_input)
                         if 0 <= card_id < len(cards):
                             selected_card = cards[card_id]
                             if player.energy >= selected_card.energy:
                                 if selected_card.heal > 0 and player.player_class == "Healer":
                                     # Enter healing mode - set pending heal card and healer player
                                     self.pending_heal_card = selected_card
                                     self.healer_player = player
                                     self.heal_target_index = 0  # reset heal target index
                                     print(f"Selected healing card: {selected_card.name}. Use A/D to choose target, Enter to confirm.")
                                 else:
                                     player.playCard(selected_card, self.boss, self.players)
                                     print(f"Player {player.id} played card: {selected_card.name}")
                             else:
                                 print("Not enough energy!")
                         else:
                             print(f"Invalid card ID: {card_id}")
                     except ValueError:
                         print("Invalid input")
                     finally:
                         self.card_input = ""

    #Checks if the turn of the player is finished to jump to the next
    def turn_finished(self, events):
     for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            print("Player Round ended")
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

     if self.phase == True:
        for player in self.players:   
                 player.energy = player.max_energy
                 player.shield = 0  
                 self.phase=False


    
     if self.victory_screen:
         self.draw_victory_screen()
         if pygame.time.get_ticks() - self.screen_timer > 3000:  # 3 seconds delay
            self.gameStateManager.players = self.players
            self.gameStateManager.set_state("ThirdLevel")  # You must define this
            
     if self.defeat_screen:
         self.draw_defeat_screen()
        
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
                self.boss.show_intention(self.players) #sets boss's new intention?
                for player in self.players:   
                    player.energy = player.max_energy  #energy reset
                    player.shield = 0                  #shield reset?Does yigioh work like that?
            pygame.display.update()                
                


class ThirdLevel:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.SysFont(None, 40)
        self.fontsmall = pygame.font.SysFont(None, 30)
        self.players = self.gameStateManager.players
        self.background = pygame.image.load("bloodydungeon.jpg")  # picture "endiktikh"
        self.round =0
        self.current_player_index=0 #index to know who the f is playing
        self.battle_over=False #Boolean for defeat screen
        self.card_input = ""
        self.selected_card = None
        self.pending_heal_card = None
        self.healer_player = None
        self.victory_screen = False
        self.defeat_screen = False
        self.screen_timer = 0 
        self.defeatscreen=pygame.image.load("defeat.png")
        self.victoryscreen=pygame.image.load("victory.jpg")
        self.phase = True
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
        self.heal_target_index = 0
        self.healthbar=pygame.image.load("healthbar.png")
        self.energyicon=pygame.image.load("energyicon.png")
        self.healingicon=pygame.image.load("healingicon.png")
      # self.armouricon=pygame.image.load("armouricon.png")
        self.swordicon=pygame.image.load("swordicon.png")
        self.shieldicon=pygame.image.load("shieldicon.png")
        self.KnightIcon=pygame.image.load("Knight.png")
        self.TankIcon=pygame.image.load("Tank.png")
        self.HealerIcon=pygame.image.load("Healer.png")
        self.AssassinIcon=pygame.image.load("Assasin.png")
        self.class_icons = {
            "Knight": self.KnightIcon,
            "Tank": self.TankIcon,
            "Healer": self.HealerIcon,
            "Assassin": self.AssassinIcon
              }
       
        player_count = len(self.players)
        self.boss = Monster(
            name="Golem", 
            max_health=int(len(self.players)*10000), 
            attack=int(len(self.players)*2500/2),  
            shield=int(len(self.players)*5000/1.5), 
            health_regen=int(len(self.players)*1000/1.5),  
            intention=[0,0,0], 
            attack_probability=4, 
            shield_probability=6)

        self.boss_image = pygame.image.load("finalboss.png").convert_alpha()
        self.boss_rect = self.boss_image.get_rect(topleft=(700,200))  
        self.bossDefeated=False
        self.boss.show_intention(self.players)


     #Check;s if monster is defeated
    def check_monster_vitals(self):
     if not self.boss.is_alive() and not self.victory_screen:
        print("The monster has been defeated")
        self.battle_over = True
        self.victory_screen = True
        self.screen_timer = pygame.time.get_ticks()  # Start timer    


    def check_team_vitals(self):
      if all(not player.is_alive() for player in self.players) and not self.defeat_screen:
        print("All players have been defeated.")
        self.battle_over = True
        self.defeat_screen = True
        self.screen_timer = pygame.time.get_ticks()  # Start timer

    def draw_victory_screen(self):
     self.display.blit(self.victoryscreen,(0,0))
     text = self.font.render("Draw 3 cards but only choose 1", True, (255, 255, 255))
     self.display.blit(text, (250, 300))

     #defeat screen
    def draw_defeat_screen(self):
     self.display.fill((0,0,0))
     self.display.blit(self.defeatscreen, (100,150))   
     

    #for monster
    def draw_health_bar(self):
     bar_width = 200
     bar_height = 20
     health_ratio = self.boss.health / self.boss.max_health
 
     # Health bar
     pygame.draw.rect(self.display, (255, 0, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width, bar_height))
     pygame.draw.rect(self.display, (0, 255, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width * health_ratio, bar_height))
 
     # Boss name
     boss_name = self.font.render(self.boss.name, True, (255, 255, 255))
     self.display.blit(boss_name, (self.boss_rect.x, self.boss_rect.y - 55))
 
     # Intention icons [attack, shield, heal]{enumerate the intentions (making a vocabulary)}
     icon_map = {0: self.swordicon, 2: self.shieldicon, 3: self.healingicon}
     icon_size = 40
     icon_spacing = 5
 
     # Count how many active intentions to center them
     active_intentions = [i for i in (0, 2, 3) if i < len(self.boss.intention) and self.boss.intention[i] == 1]
     active_count = len(active_intentions)
     start_x = self.boss_rect.x + (self.boss_rect.width // 2) - ((icon_size + icon_spacing) * active_count - icon_spacing) // 2
     icon_y = self.boss_rect.y - 80
 
     # Draw each active icon
     icon_x = start_x
     for i in active_intentions:
         icon = pygame.transform.scale(icon_map[i], (icon_size, icon_size))
         self.display.blit(icon, (icon_x, icon_y))
         icon_x += icon_size + icon_spacing


     #for players
    def draw_player_bars(self, player, rect):
     full_bar_width = 100
     health_bar_height = 10
     energy_bar_height = 5
    
     healthbar_bg = pygame.transform.scale(self.healthbar, (120, 14))  # Adjust if needed
     healthbar_pos = (rect.x - 20, rect.y - 28)  # Position it slightly to the left of the player sprite
     self.display.blit(healthbar_bg, healthbar_pos)
 
     # Calculate filled health portion
     health_ratio = player.health / player.max_health
     fill_width = int(102* health_ratio)  # The fillable part of the bar inside (approximate)
     fill_height = 5
     fill_x = healthbar_pos[0] + 16  # Start of the green fill inside the image
     fill_y = healthbar_pos[1] + 5  # Vertically centered

    # Draw the green fill bar (actual health)
     pygame.draw.rect(self.display, (0, 255, 0), (fill_x, fill_y, fill_width, fill_height))
     
     # Energy bar (Gray background, Blue foreground — thinner)
     energy_ratio = player.energy / player.max_energy
     pygame.draw.rect(self.display, (50, 50, 50), (rect.x, rect.y - 12, full_bar_width, energy_bar_height))
     pygame.draw.rect(self.display, (0, 0, 255), (rect.x, rect.y - 12, full_bar_width * energy_ratio, energy_bar_height))
  
     icon_size = 12  # Resize icon to fit nicely
     resized_icon = pygame.transform.scale(self.energyicon, (icon_size, icon_size))
     icon_x = rect.x - icon_size - 3  # 5 pixels gap from the bar
     icon_y = rect.y - 12  # Align with energy bar
     self.display.blit(resized_icon, (icon_x, icon_y))


     # Optional: Draw player name/ID above bars
     player_name = self.font.render(f"P{player.id}", True, (255, 255, 255))
     self.display.blit(player_name, (rect.x, rect.y - 45))
     # Draw arrow if healer is selecting a target
     
    def get_class_icon(self, player):
     if player.player_class == "Knight":
        return self.KnightIcon
     elif player.player_class == "Tank":
        return self.TankIcon
     elif player.player_class == "Healer":
        return self.HealerIcon
     elif player.player_class == "Assassin":
         return self.AssassinIcon
     else:
        return pygame.Surface((100, 40))  # fallback blank surface if unknown class

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
        icon = self.get_class_icon(player)
        icon_resized = pygame.transform.scale(icon, (box_width, box_height))
        self.display.blit(icon_resized, (x, y))

       
        if self.pending_heal_card and self.healer_player is not None and self.heal_target_index == i:
         arrow_rect = self.arrow_image.get_rect(center=(x + box_width // 2, y - 60))
         self.display.blit(self.arrow_image, arrow_rect)


    #Maybe it needs modifications {San to PlayerTurn}
    def handle_player_turn(self, player, events):
    # 1. Healing target selection mode: handle arrow keys, confirm, cancel
     if self.pending_heal_card and self.healer_player == player:
         for event in events:
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_a:
                     self.heal_target_index = (self.heal_target_index - 1) % len(self.players)
                     while not self.players[self.heal_target_index].is_alive():
                         self.heal_target_index = (self.heal_target_index - 1) % len(self.players)

                 elif event.key == pygame.K_d:
                     self.heal_target_index = (self.heal_target_index + 1) % len(self.players)
                     while not self.players[self.heal_target_index].is_alive():
                         self.heal_target_index = (self.heal_target_index + 1) % len(self.players)

                 elif event.key == pygame.K_RETURN:
                     target_player = self.players[self.heal_target_index]
                     if target_player.is_alive():
                         self.healer_player.playCard(self.pending_heal_card, self.boss, self.players, target=target_player)
                         self.pending_heal_card = None
                         self.healer_player = None
                         print("Healing complete.")
                     else:
                         print("Selected player is not alive!")

                 elif event.key == pygame.K_ESCAPE:
                     print("Healing cancelled.")
                     self.pending_heal_card = None
                     self.healer_player = None
         return  # Skip the rest of the turn while healing target selecting

     # 2. Normal card input mode
     for event in events:
         if event.type == pygame.KEYDOWN:
             if event.unicode.isdigit():
                 self.card_input += event.unicode
                 print(f"Card ID input: {self.card_input}")

             elif event.key == pygame.K_BACKSPACE:
                 self.card_input = self.card_input[:-1]

             elif event.key == pygame.K_RETURN:
                 if self.card_input:
                     try:
                         card_id = int(self.card_input)
                         if 0 <= card_id < len(cards):
                             selected_card = cards[card_id]
                             if player.energy >= selected_card.energy:
                                 if selected_card.heal > 0 and player.player_class == "Healer":
                                     # Enter healing mode - set pending heal card and healer player
                                     self.pending_heal_card = selected_card
                                     self.healer_player = player
                                     self.heal_target_index = 0  # reset heal target index
                                     print(f"Selected healing card: {selected_card.name}. Use A/D to choose target, Enter to confirm.")
                                 else:
                                     player.playCard(selected_card, self.boss, self.players)
                                     print(f"Player {player.id} played card: {selected_card.name}")
                             else:
                                 print("Not enough energy!")
                         else:
                             print(f"Invalid card ID: {card_id}")
                     except ValueError:
                         print("Invalid input")
                     finally:
                         self.card_input = ""

    #Checks if the turn of the player is finished to jump to the next
    def turn_finished(self, events):
     for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            print("Player Round ended")
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

     if self.phase == True:
        for player in self.players:   
                 player.energy = player.max_energy
                 player.shield = 0  
                 self.phase=False


    
     if self.victory_screen:
         self.draw_victory_screen()
         if pygame.time.get_ticks() - self.screen_timer > 3000:  # 3 seconds delay
            self.gameStateManager.players = self.players
            self.gameStateManager.set_state("ThirdLevel")  # You must define this
            
     if self.defeat_screen:
         self.draw_defeat_screen()
        
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
                self.boss.show_intention(self.players) #sets boss's new intention?
                for player in self.players:   
                    player.energy = player.max_energy  #energy reset
                    player.shield = 0                  #shield reset?Does yigioh work like that?
            pygame.display.update()                


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