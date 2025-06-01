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
        self.defeatscreen=pygame.image.load("defeat.jpg")
        self.victoryscreen=pygame.image.load("victory.jpg")
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
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
     self.display.blit(self.defeatscreen, (0, 0))   
     
    #for monster
    def draw_health_bar(self):
        bar_width=200
        bar_height=20
        health_ratio =self.boss.health/self.boss.max_health #ousiastika poso posostiaia peftei to hp
        pygame.draw.rect(self.display,(255,0,0),(self.boss_rect.x,self.boss_rect.y-30,bar_width,bar_height))
        pygame.draw.rect(self.display, (0, 255, 0), (self.boss_rect.x, self.boss_rect.y - 30, bar_width * health_ratio, bar_height))
        boss_name=self.font.render(self.boss.name,True,(255,255,255))
        self.display.blit(boss_name,(self.boss_rect.x,self.boss_rect.y-55))
        intention_text = self.font.render(f"Intentions: {self.boss.intention}", True, (255, 255, 0))
        self.display.blit(intention_text, (self.boss_rect.x, self.boss_rect.y + 160))



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
     # Draw arrow if healer is selecting a target
     


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
        if self.pending_heal_card and self.healer_player is not None and self.heal_target_index == i:
         arrow_rect = self.arrow_image.get_rect(center=(x + box_width // 2, y - 60))
         self.display.blit(self.arrow_image, arrow_rect)



      #Maybe it needs modifications {San to PlayerTurn}
    def handle_player_turn(self, player, events):
     # Waiting for heal target selection
      if self.pending_heal_card and self.healer_player == player:
          for event in events:
              if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                  target_index = int(event.unicode) - 1
                  if 0 <= target_index < len(self.players):
                      target_player = self.players[target_index]
                      if target_player.is_alive():
                          self.healer_player.playCard(self.pending_heal_card, self.boss, self.players, target=target_player)
                          self.pending_heal_card = None
                          self.healer_player = None
                          print("Healing complete.")
                      else:
                          print("Selected player is not alive!")
                  else:
                     print("Invalid player index for healing.")
          return  # Skip the rest until healing is done
 
       # Standard input and card selection
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
                                      # Switch to heal selection mode
                                      self.pending_heal_card = selected_card
                                      self.healer_player = player
                                      print(f"Selected healing card: {selected_card.name}. Now press the number of the player to heal.")
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
