import pygame
import sys
from player import Knight, Tank, Assassin, Healer
from card import Card, cards
from monster import Monster

# Constants
SCREENWIDTH = 1000
SCREENHEIGHT = 600
FPS = 60

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        self.players = []
        self.playercount = 0

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        if state is not None:  # Ensure we never set state to None
            self.currentState = state

    def get_playercount(self):
        return self.playercount

    def set_playercount(self, playercount):
        self.playercount = playercount

class BaseLevel:
    def __init__(self, display, gameStateManager, background_img, boss_img, boss_stats):
        self.display = display
        self.gameStateManager = gameStateManager
        self.background = pygame.image.load(background_img)
        self.font = pygame.font.SysFont(None, 40)
        self.fontsmall = pygame.font.SysFont(None, 30)
        
        # Player tracking
        self.players = self.gameStateManager.players
        self.current_player_index = 0
        self.round = 0
        
        # Card handling
        self.card_input = ""
        self.selected_card = None
        self.pending_heal_card = None
        self.healer_player = None
        self.heal_target_index = 0
        
        # Game state
        self.battle_over = False
        self.victory_screen = False
        self.defeat_screen = False
        self.screen_timer = 0
        self.phase = True
        
        # Load assets
        self.load_assets()
        
        # Boss setup
        self.setup_boss(boss_img, boss_stats)
        
    def load_assets(self):
        """Load common game assets"""
        self.defeatscreen = pygame.image.load("defeat.png")
        self.victoryscreen = pygame.image.load("victory.jpg")
        self.arrow_image = pygame.image.load("arrow.png").convert_alpha()
        self.healthbar = pygame.image.load("healthbar.png")
        self.energyicon = pygame.image.load("energyicon.png")
        self.healingicon = pygame.image.load("healingicon.png").convert_alpha()
        self.swordicon = pygame.image.load("swordicon.png").convert_alpha()
        self.shieldicon = pygame.image.load("shieldicon.png").convert_alpha()
        
        # Class icons
        self.KnightIcon = pygame.image.load("Knight.png")
        self.TankIcon = pygame.image.load("Tank.png")
        self.HealerIcon = pygame.image.load("Healer.png")
        self.AssassinIcon = pygame.image.load("Assasin.png")
        
        self.class_icons = {
            "Knight": self.KnightIcon,
            "Tank": self.TankIcon,
            "Healer": self.HealerIcon,
            "Assassin": self.AssassinIcon
        }
    
    def setup_boss(self, boss_img, boss_stats):
        """Initialize the boss with given stats"""
        self.boss = Monster(**boss_stats)
        self.boss_image = pygame.image.load(boss_img).convert_alpha()
        self.boss_rect = self.boss_image.get_rect(topleft=(700, 200))
        self.bossDefeated = False
        self.boss.show_intention(self.players)
    
    def reset_player_resources(self):
        """Reset player energy and shield at start of level"""
        if self.phase:
            for player in self.players:
                player.energy = player.max_energy
                player.shield = 0
            self.phase = False
    
    def check_monster_vitals(self):
        if not self.boss.is_alive() and not self.victory_screen:
            print("The monster has been defeated")
            self.battle_over = True
            self.victory_screen = True
            self.screen_timer = pygame.time.get_ticks()

    def check_team_vitals(self):
        if all(not player.is_alive() for player in self.players) and not self.defeat_screen:
            print("All players have been defeated.")
            self.battle_over = True
            self.defeat_screen = True
            self.screen_timer = pygame.time.get_ticks()

    def draw_victory_screen(self):
        self.display.blit(self.victoryscreen, (0, 0))
        text = self.font.render("Draw 3 cards but only choose 1", True, (255, 255, 255))
        self.display.blit(text, (250, 300))

    def draw_defeat_screen(self):
        self.display.fill((0, 0, 0))
        self.display.blit(self.defeatscreen, (100, 150))
    
    def draw_health_bar(self):
        bar_width = 200
        bar_height = 20
        health_ratio = self.boss.health / self.boss.max_health
        
        # Health bar
        pygame.draw.rect(self.display, (255, 0, 0), 
                         (self.boss_rect.x, self.boss_rect.y - 30, bar_width, bar_height))
        pygame.draw.rect(self.display, (0, 255, 0), 
                         (self.boss_rect.x, self.boss_rect.y - 30, bar_width * health_ratio, bar_height))
        
        # Boss name
        boss_name = self.font.render(self.boss.name, True, (255, 255, 255))
        self.display.blit(boss_name, (self.boss_rect.x, self.boss_rect.y - 55))
        
        # Intention icons
        icon_map = {0: self.swordicon, 2: self.shieldicon, 3: self.healingicon}
        icon_size = 40
        icon_spacing = 5
        
        active_intentions = [i for i in (0, 2, 3) 
                            if i < len(self.boss.intention) and self.boss.intention[i] == 1]
        active_count = len(active_intentions)
        start_x = self.boss_rect.x + (self.boss_rect.width // 2) - ((icon_size + icon_spacing) * active_count - icon_spacing) // 2
        icon_y = self.boss_rect.y - 80
        
        icon_x = start_x
        for i in active_intentions:
            icon = pygame.transform.scale(icon_map[i], (icon_size, icon_size))
            self.display.blit(icon, (icon_x, icon_y))
            icon_x += icon_size + icon_spacing

    def draw_player_bars(self, player, rect):
        full_bar_width = 100
        health_bar_height = 10
        energy_bar_height = 5
        
        healthbar_bg = pygame.transform.scale(self.healthbar, (120, 14))
        healthbar_pos = (rect.x - 20, rect.y - 28)
        self.display.blit(healthbar_bg, healthbar_pos)
        
        health_ratio = player.health / player.max_health
        fill_width = int(102 * health_ratio)
        fill_height = 5
        fill_x = healthbar_pos[0] + 16
        fill_y = healthbar_pos[1] + 5
        
        pygame.draw.rect(self.display, (0, 255, 0), (fill_x, fill_y, fill_width, fill_height))
        
        energy_ratio = player.energy / player.max_energy
        pygame.draw.rect(self.display, (50, 50, 50), (rect.x, rect.y - 12, full_bar_width, energy_bar_height))
        pygame.draw.rect(self.display, (0, 0, 255), (rect.x, rect.y - 12, full_bar_width * energy_ratio, energy_bar_height))
        
        icon_size = 12
        resized_icon = pygame.transform.scale(self.energyicon, (icon_size, icon_size))
        self.display.blit(resized_icon, (rect.x - icon_size - 3, rect.y - 12))
        
        player_name = self.font.render(f"P{player.id}", True, (255, 255, 255))
        self.display.blit(player_name, (rect.x, rect.y - 45))

    def get_class_icon(self, player):
        return self.class_icons.get(player.player_class, pygame.Surface((100, 40)))

    def draw_players(self):
        start_x = 50
        start_y = 500
        box_width = 100
        box_height = 100
        gap = 120
        
        for i, player in enumerate(self.players):
            x = start_x + i * gap
            y = start_y
            rect = pygame.Rect(x, y, box_width, box_height)
            
            self.draw_player_bars(player, rect)
            icon = self.get_class_icon(player)
            icon_resized = pygame.transform.scale(icon, (box_width, box_height))
            self.display.blit(icon_resized, (x, y))
            
            if self.pending_heal_card and self.healer_player is not None and self.heal_target_index == i:
                arrow_rect = self.arrow_image.get_rect(center=(x + box_width // 2, y - 60))
                self.display.blit(self.arrow_image, arrow_rect)

    def handle_player_turn(self, player, events):
        if self.pending_heal_card and self.healer_player == player:
            self.handle_heal_target_selection(events)
            return
        
        self.handle_card_selection(player, events)

    def handle_heal_target_selection(self, events):
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

    def handle_card_selection(self, player, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    self.card_input += event.unicode
                    print(f"Card ID input: {self.card_input}")
                elif event.key == pygame.K_BACKSPACE:
                    self.card_input = self.card_input[:-1]
                elif event.key == pygame.K_RETURN and self.card_input:
                    try:
                        card_id = int(self.card_input)
                        if 0 <= card_id < len(cards):
                            selected_card = cards[card_id]
                            if player.energy >= selected_card.energy:
                                if selected_card.heal > 0 and player.player_class == "Healer":
                                    self.pending_heal_card = selected_card
                                    self.healer_player = player
                                    self.heal_target_index = 0
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

    def turn_finished(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                print("Player Round ended")
                return True
        return False

    def monster_turn(self):
        if self.boss.intention[0] == 1:
            target = self.players[self.boss.intention[1] - 1]
            if target.is_alive():
                self.boss.do_damage(self.boss.attack, target)
                print(f"{self.boss.name} attacked Player {target.id} for {self.boss.attack} damage!")
        if self.boss.intention[2] == 1:
            self.boss.gain_shield()
            print(f"{self.boss.name} gained {self.boss.shield} shield!")
        self.boss.heal()

    def run(self, events):
        self.reset_player_resources()
        
        if self.victory_screen:
            self.draw_victory_screen()
            if pygame.time.get_ticks() - self.screen_timer > 3000:
                self.gameStateManager.players = self.players
                self.gameStateManager.set_state(self.next_level)
                
        if self.defeat_screen:
            self.draw_defeat_screen()
            
        if self.battle_over:
            return

        self.display.blit(self.background, (0, 0))
        self.display.blit(self.boss_image, self.boss_rect)
        self.draw_health_bar()
        self.draw_players()

        self.check_monster_vitals()
        self.check_team_vitals()
        
        if self.bossDefeated or self.battle_over:
            return

        current_player = self.players[self.current_player_index]
        if current_player.is_alive():
            self.handle_player_turn(current_player, events)

        if self.turn_finished(events):
            self.current_player_index += 1
            if self.current_player_index >= len(self.players):
                self.monster_turn()
                self.current_player_index = 0
                self.round += 1
                self.boss.show_intention(self.players)
                for player in self.players:
                    player.energy = player.max_energy
                    player.shield = 0
                    
        pygame.display.update()

class FirstLevel(BaseLevel):
    def __init__(self, gameStateManager, display):
        boss_stats = {
            "name": "Rekanos",
            "max_health": int(len(gameStateManager.players) * 5000),
            "attack": int(len(gameStateManager.players) * 1000 / 2),
            "shield": int(len(gameStateManager.players) * 1000 / 1.5),
            "health_regen": 0,
            "intention": [0, 0, 0],
            "attack_probability": 5,
            "shield_probability": 5
        }
        super().__init__(display, gameStateManager, "swamptower.jpg", "firstboss.jpg", boss_stats)
        self.next_level = "SecondLevel"

class SecondLevel(BaseLevel):
    def __init__(self, display, gameStateManager):
        boss_stats = {
            "name": "Gorgon",
            "max_health": int(len(gameStateManager.players) * 8000),
            "attack": int(len(gameStateManager.players) * 2000 / 2),
            "shield": int(len(gameStateManager.players) * 3000 / 1.5),
            "health_regen": int(len(gameStateManager.players) * 500 / 1.5),
            "intention": [0, 0, 0],
            "attack_probability": 6,
            "shield_probability": 6
        }
        super().__init__(display, gameStateManager, "lonelybridge.jpg", "secondboss.png", boss_stats)
        self.next_level = "ThirdLevel"

class ThirdLevel(BaseLevel):
    def __init__(self, display, gameStateManager):
        boss_stats = {
            "name": "Golem",
            "max_health": int(len(gameStateManager.players) * 10000),
            "attack": int(len(gameStateManager.players) * 2500 / 2),
            "shield": int(len(gameStateManager.players) * 5000 / 1.5),
            "health_regen": int(len(gameStateManager.players) * 1000 / 1.5),
            "intention": [0, 0, 0],
            "attack_probability": 4,
            "shield_probability": 6
        }
        super().__init__(display, gameStateManager, "bloodydungeon.jpg", "finalboss.png", boss_stats)
        self.next_level = "Menu"  # Return to menu after final level

class CharacterSelect:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.background = pygame.image.load('background.png')
        self.gameStateManager = gameStateManager
        self.player_count = self.gameStateManager.playercount
        self.font = pygame.font.SysFont(None, 60)

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
                elif event.key == pygame.K_SPACE:
                    self.gameStateManager.set_playercount(self.player_count)
                    self.gameStateManager.set_state("CharacterClass")

        self.display.blit(self.background, (0, 0))
        pygame.draw.rect(self.display, (169, 169, 169), (350, 250, 300, 100))
        text_surface = self.font.render(f'Players: {self.player_count}', True, (0, 0, 0))
        self.display.blit(text_surface, (400, 275))
        confirm_surface = self.font.render('Press SPACE to confirm', True, (255, 255, 255))
        self.display.blit(confirm_surface, (300, 200))

class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.button = pygame.image.load("start_btn.png")
        self.background = pygame.image.load('background.png')
    
    def run(self, events):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.button, (300, 100))
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
        self.phase = 0
        self.frame_counter = 0
        
        # Load class icons
        self.KnightIcon = pygame.image.load("Knight.png")
        self.TankIcon = pygame.image.load("Tank.png")
        self.HealerIcon = pygame.image.load("Healer.png")
        self.AssassinIcon = pygame.image.load("Assasin.png")
        
        self.class_icons = {
            "Knight": self.KnightIcon,
            "Tank": self.TankIcon,
            "Healer": self.HealerIcon,
            "Assassin": self.AssassinIcon
        }

    def run(self, events):
        self.display.fill((0, 0, 0))
        
        if self.phase == 0:
            self.handle_class_selection(events)
        elif self.phase == 1:
            self.show_player_stats()
        elif self.phase == 2:
            self.show_transition_message()
        elif self.phase == 3:
            self.gameStateManager.set_state("FirstLevel")
            
        pygame.display.update()

    def handle_class_selection(self, events):
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
            if self.frame_counter > 180:
                self.class_selected = True
                self.phase = 1
                self.frame_counter = 0
                self.gameStateManager.players = self.players

    def show_player_stats(self):
        screen_width = SCREENWIDTH
        screen_height = SCREENHEIGHT
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

            icon = self.class_icons.get(player.player_class)
            if icon:
                icon_rect = icon.get_rect(center=(center_x, center_y - 40))
                self.display.blit(icon, icon_rect)

            text_surface = self.font.render(player.__class__.__name__, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(center_x, center_y + 40))
            self.display.blit(text_surface, text_rect)

            energy_surface = self.fontsmall.render(f"Max Energy: {player.max_energy}", True, (255, 255, 255))
            energy_rect = energy_surface.get_rect(center=(center_x, center_y + 65))
            self.display.blit(energy_surface, energy_rect)

            health_surface = self.fontsmall.render(f"Max Health: {player.max_health}", True, (255, 255, 255))
            health_rect = health_surface.get_rect(center=(center_x, center_y + 85))
            self.display.blit(health_surface, health_rect)

            class_color = {
                "Knight": (255, 0, 0),
                "Tank": (0, 255, 0),
                "Healer": (0, 0, 255),
                "Assassin": (255, 255, 0)
            }.get(player.player_class, (100, 100, 100))

            pygame.draw.rect(self.display, class_color, (center_x - 50, center_y + 105, 100, 10))

        self.frame_counter += 1
        if self.frame_counter > 600:
            self.frame_counter = 0
            self.phase = 2

    def show_transition_message(self):
        self.display.fill((0, 0, 0))
        message = self.font.render("The journey of our Heroes starts", True, (255, 87, 51))
        self.display.blit(message, (200, 280))
        self.frame_counter += 1
        if self.frame_counter > 300:
            self.phase = 3

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager('Menu')

        self.menu = Menu(self.screen, self.gameStateManager)
        self.charactersel = CharacterSelect(self.screen, self.gameStateManager)
        self.characterclass = None
        self.firstlevel = None
        self.secondlevel = None
        self.thirdlevel = None
        
        self.states = {
            "Menu": self.menu,
            "CharacterSelect": self.charactersel,
            # Initialize other states as None, they'll be created when needed
            "CharacterClass": None,
            "FirstLevel": None,
            "SecondLevel": None,
            "ThirdLevel": None
        }

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.gameStateManager.get_state() == "Menu":
                    self.gameStateManager.set_state("CharacterSelect")

            current_state = self.gameStateManager.get_state()
            
            # Ensure we have a valid state
            if current_state is None:
                current_state = "Menu"
                self.gameStateManager.set_state(current_state)

            # Lazy initialization of game states
            if current_state == "CharacterClass" and self.states["CharacterClass"] is None:
                self.characterclass = CharacterClass(self.screen, self.gameStateManager)
                self.states["CharacterClass"] = self.characterclass
            elif current_state == "FirstLevel" and self.states["FirstLevel"] is None:
                self.firstlevel = FirstLevel(self.gameStateManager, self.screen)
                self.states["FirstLevel"] = self.firstlevel
            elif current_state == "SecondLevel" and self.states["SecondLevel"] is None:
                self.secondlevel = SecondLevel(self.screen, self.gameStateManager)
                self.states["SecondLevel"] = self.secondlevel
            elif current_state == "ThirdLevel" and self.states["ThirdLevel"] is None:
                self.thirdlevel = ThirdLevel(self.screen, self.gameStateManager)
                self.states["ThirdLevel"] = self.thirdlevel

            # Run the current state if it exists
            if self.states[current_state] is not None:
                self.states[current_state].run(events)
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()