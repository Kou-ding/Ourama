import pygame
import random
import sys
from pygame.locals import *

# Assuming card.py, player.py, and monster.py are in the same directory
from card import cards
from player import Player, Knight, Assassin, Healer, Tank
from monster import Monster

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fonts
TITLE_FONT = pygame.font.SysFont('arial', 50, bold=True)
LARGE_FONT = pygame.font.SysFont('arial', 36)
MEDIUM_FONT = pygame.font.SysFont('arial', 24)
SMALL_FONT = pygame.font.SysFont('arial', 18)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=DARK_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        text_surf = MEDIUM_FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class CardDisplay:
    def __init__(self, x, y, card, width=150, height=200):
        self.rect = pygame.Rect(x, y, width, height)
        self.card = card
        self.width = width
        self.height = height
        self.selected = False
        
    def draw(self, surface):
        color = YELLOW if self.selected else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        # Card title
        title = SMALL_FONT.render(self.card.name, True, BLACK)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.y + 20))
        surface.blit(title, title_rect)
        
        # Card description (simplified)
        desc = SMALL_FONT.render(f"Cost: {self.card.cost}", True, BLACK)
        desc_rect = desc.get_rect(topleft=(self.rect.x + 10, self.rect.y + 50))
        surface.blit(desc, desc_rect)
        
        # Card effect
        effect_lines = self._wrap_text(self.card.description, SMALL_FONT, self.width - 20)
        for i, line in enumerate(effect_lines):
            effect_text = SMALL_FONT.render(line, True, BLACK)
            surface.blit(effect_text, (self.rect.x + 10, self.rect.y + 80 + i * 20))
    
    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
    
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Game:
    def __init__(self):
        self.players = []
        self.current_round = 0
        self.monsters = []
        self.current_player = None
        self.current_monster = None
        self.current_card = None
        self.monsterDefeated = False
        self.game_state = "setup"  # setup, player_turn, monster_turn, game_over
        self.selected_player_class = None
        self.selected_card_index = None
        self.message = "Welcome to Ourama!"
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ourama Card Game")
        self.clock = pygame.time.Clock()
        
        # UI elements
        self.class_buttons = [
            Button(SCREEN_WIDTH//2 - 200, 200, 300, 50, "1. Knight"),
            Button(SCREEN_WIDTH//2 - 200, 270, 300, 50, "2. Assassin"),
            Button(SCREEN_WIDTH//2 - 200, 340, 300, 50, "3. Healer"),
            Button(SCREEN_WIDTH//2 - 200, 410, 300, 50, "4. Tank")
        ]
        
        self.num_players_buttons = [
            Button(SCREEN_WIDTH//2 - 150, 200, 100, 50, "1"),
            Button(SCREEN_WIDTH//2 - 50, 200, 100, 50, "2"),
            Button(SCREEN_WIDTH//2 + 50, 200, 100, 50, "3"),
            Button(SCREEN_WIDTH//2 + 150, 200, 100, 50, "4")
        ]
        
        self.end_turn_button = Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80, 150, 50, "End Turn")
        
    def draw_text(self, text, font, color, x, y, centered=False):
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
        
    def draw_health_bar(self, x, y, width, height, current, max_val, color=GREEN):
        ratio = current / max_val
        pygame.draw.rect(self.screen, BLACK, (x-2, y-2, width+4, height+4), 0)
        pygame.draw.rect(self.screen, RED, (x, y, width, height), 0)
        pygame.draw.rect(self.screen, color, (x, y, width * ratio, height), 0)
        
    def draw_shield_bar(self, x, y, width, height, current):
        if current > 0:
            pygame.draw.rect(self.screen, BLUE, (x, y, width, height), 0)
            shield_text = SMALL_FONT.render(f"{current}", True, WHITE)
            self.screen.blit(shield_text, (x + width + 5, y))
        
    def draw_energy_bar(self, x, y, width, height, current, max_val):
        for i in range(max_val):
            color = YELLOW if i < current else DARK_GRAY
            pygame.draw.rect(self.screen, color, (x + i * (width//max_val), y, width//max_val - 2, height), 0)
    
    def initPlayersMonsters(self):
        # Initialize 3 Monsters
        self.monsters = [None] * 3
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
        
        self.message = "Players and Monsters have been initialized!"
        self.game_state = "player_turn"
        self.current_monster = self.monsters[0]
    
    def playerTurn(self, player):
        # Reset player energy and shield at the start of each turn
        player.energy = player.max_energy
        player.shield = 0
        
        # Draw 2 cards (simplified for demo)
        # In a full implementation, you'd manage the player's hand properly
        
        self.current_player = player
        self.message = f"Player {player.id}'s turn - Play a card or end turn"
    
    def playCard(self, card_index):
        if card_index is not None and card_index < len(self.current_player.hand):
            card = self.current_player.hand[card_index]
            if self.current_player.energy >= card.cost:
                self.current_player.playCard(card, self.current_monster, self.players)
                self.message = f"Player {self.current_player.id} played {card.name}!"
                self.checkMonsterVitals()
                return True
            else:
                self.message = f"Not enough energy to play {card.name}!"
                return False
        return False
    
    def monsterTurn(self):
        self.message = f"{self.current_monster.name}'s turn"
        
        if self.current_monster.intention[0] == 1:
            # Attack a random player
            target = self.players[self.current_monster.intention[1]-1]
            self.current_monster.do_damage(self.current_monster.attack, target)
            self.message = f"{self.current_monster.name} attacked Player {target.id} for {self.current_monster.attack} damage!"
        if self.current_monster.intention[2] == 1:
            # Gain shield
            self.current_monster.gain_shield()
            self.message = f"{self.current_monster.name} gained {self.current_monster.shield} shield!"
        self.current_monster.heal()
        
        # Check if any player is alive
        self.checkTeamVitals()
        
        # Next player's turn
        self.game_state = "player_turn"
        next_player_index = self.players.index(self.current_player) + 1 if self.current_player else 0
        if next_player_index >= len(self.players):
            next_player_index = 0
            self.current_round += 1
            self.current_monster.show_intention(len(self.players))
        
        # Find next alive player
        for i in range(len(self.players)):
            player = self.players[(next_player_index + i) % len(self.players)]
            if player.is_alive():
                self.playerTurn(player)
                return
        
        # If no players left (should be caught by checkTeamVitals)
        self.game_state = "game_over"
    
    def checkTeamVitals(self):
        endScreen = True
        for player in self.players:
            if player.is_alive():
                endScreen = False
        if endScreen:
            self.message = "Game Over! All players have been defeated."
            self.game_state = "game_over"
    
    def checkMonsterVitals(self):
        if not self.current_monster.is_alive():
            self.message = f"{self.current_monster.name} has been defeated!"
            self.monsterDefeated = True
            
            # Move to next monster or end game
            next_monster_index = self.monsters.index(self.current_monster) + 1
            if next_monster_index < len(self.monsters):
                self.current_monster = self.monsters[next_monster_index]
                self.monsterDefeated = False
                self.current_round = 0
                self.message = f"You have encountered {self.current_monster.name}!"
            else:
                self.message = "You Win! All monsters have been defeated."
                self.game_state = "game_over"
    
    def playEncounter(self, monster):
        self.current_monster = monster
        self.message = f"You have encountered {monster.name}!"
        self.current_round = 0
        self.monsterDefeated = False
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEMOTION:
                # Check button hovers
                if self.game_state == "setup":
                    for button in self.num_players_buttons:
                        button.check_hover(mouse_pos)
                elif self.game_state == "class_selection":
                    for button in self.class_buttons:
                        button.check_hover(mouse_pos)
                elif self.game_state == "player_turn":
                    self.end_turn_button.check_hover(mouse_pos)
                    
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == "setup":
                    for i, button in enumerate(self.num_players_buttons):
                        if button.is_clicked(mouse_pos, event):
                            num_players = i + 1
                            self.players = [None] * num_players
                            self.game_state = "class_selection"
                            self.message = "Select classes for each player"
                            self.current_player_selection = 0
                
                elif self.game_state == "class_selection":
                    for i, button in enumerate(self.class_buttons):
                        if button.is_clicked(mouse_pos, event):
                            if i == 0:
                                self.players[self.current_player_selection] = Knight(self.current_player_selection+1)
                            elif i == 1:
                                self.players[self.current_player_selection] = Assassin(self.current_player_selection+1)
                            elif i == 2:
                                self.players[self.current_player_selection] = Healer(self.current_player_selection+1)
                            elif i == 3:
                                self.players[self.current_player_selection] = Tank(self.current_player_selection+1)
                            
                            self.current_player_selection += 1
                            if self.current_player_selection >= len(self.players):
                                self.initPlayersMonsters()
                            else:
                                self.message = f"Select class for Player {self.current_player_selection+1}"
                
                elif self.game_state == "player_turn":
                    if self.end_turn_button.is_clicked(mouse_pos, event):
                        self.game_state = "monster_turn"
                        self.monsterTurn()
                    
                    # Check card clicks (simplified - in a real game, you'd have proper card selection)
                    # This is just a placeholder for the card playing logic
                    if self.current_player and self.current_player.hand:
                        card_width = 150
                        card_height = 200
                        start_x = (SCREEN_WIDTH - (len(self.current_player.hand) * (card_width + 10))) // 2
                        
                        for i in range(len(self.current_player.hand)):
                            card_rect = pygame.Rect(start_x + i * (card_width + 10), 
                                                  SCREEN_HEIGHT - card_height - 20, 
                                                  card_width, card_height)
                            if card_rect.collidepoint(mouse_pos):
                                if self.playCard(i):
                                    # Card played successfully
                                    pass
                
                elif self.game_state == "game_over":
                    # Add restart button logic here if desired
                    pass
    
    def render(self):
        self.screen.fill(WHITE)
        
        # Draw game title/message
        self.draw_text("Ourama", TITLE_FONT, BLACK, SCREEN_WIDTH//2, 50, centered=True)
        self.draw_text(self.message, MEDIUM_FONT, BLACK, SCREEN_WIDTH//2, 120, centered=True)
        
        if self.game_state == "setup":
            self.draw_text("How many players are there?", LARGE_FONT, BLACK, SCREEN_WIDTH//2, 150, centered=True)
            for button in self.num_players_buttons:
                button.draw(self.screen)
                
        elif self.game_state == "class_selection":
            self.draw_text("Select your class:", LARGE_FONT, BLACK, SCREEN_WIDTH//2, 150, centered=True)
            for button in self.class_buttons:
                button.draw(self.screen)
                
        elif self.game_state in ["player_turn", "monster_turn"]:
            # Draw current round
            self.draw_text(f"Round {self.current_round}", MEDIUM_FONT, BLACK, 20, 20)
            
            # Draw monster info
            if self.current_monster:
                # Monster stats
                self.draw_text(f"{self.current_monster.name}", LARGE_FONT, BLACK, SCREEN_WIDTH//2, 20, centered=True)
                self.draw_health_bar(SCREEN_WIDTH//2 - 150, 50, 300, 20, self.current_monster.health, self.current_monster.max_health)
                self.draw_shield_bar(SCREEN_WIDTH//2 - 150, 80, 300, 10, self.current_monster.current_shield)
                
                # Monster intentions
                intent_text = ""
                if self.current_monster.intention[0] == 1:
                    intent_text = f"Will attack Player {self.current_monster.intention[1]}"
                elif self.current_monster.intention[2] == 1:
                    intent_text = "Will gain shield"
                self.draw_text(f"Intent: {intent_text}", MEDIUM_FONT, BLACK, SCREEN_WIDTH//2, 100, centered=True)
            
            # Draw players info
            player_width = 200
            player_spacing = (SCREEN_WIDTH - (len(self.players) * player_width)) // (len(self.players) + 1)
            
            for i, player in enumerate(self.players):
                x = player_spacing + i * (player_width + player_spacing)
                y = 150
                
                # Player background (highlight current player)
                if player == self.current_player and self.game_state == "player_turn":
                    pygame.draw.rect(self.screen, YELLOW, (x-10, y-10, player_width+20, 180))
                
                # Player info
                pygame.draw.rect(self.screen, GRAY, (x, y, player_width, 160))
                pygame.draw.rect(self.screen, BLACK, (x, y, player_width, 160), 2)
                
                self.draw_text(f"Player {player.id}", MEDIUM_FONT, BLACK, x + player_width//2, y + 20, centered=True)
                self.draw_text(player.__class__.__name__, SMALL_FONT, BLACK, x + player_width//2, y + 50, centered=True)
                
                # Health and shield
                self.draw_health_bar(x + 20, y + 80, 160, 15, player.health, player.max_health)
                self.draw_shield_bar(x + 20, y + 100, 160, 10, player.shield)
                
                # Energy
                self.draw_text("Energy:", SMALL_FONT, BLACK, x + 20, y + 120)
                self.draw_energy_bar(x + 80, y + 120, 100, 15, player.energy, player.max_energy)
                
                # Status (alive/dead)
                status = "ALIVE" if player.is_alive() else "DEFEATED"
                status_color = GREEN if player.is_alive() else RED
                self.draw_text(status, SMALL_FONT, status_color, x + player_width//2, y + 140, centered=True)
            
            # Draw cards in hand (simplified)
            if self.game_state == "player_turn" and self.current_player and self.current_player.is_alive():
                # Draw end turn button
                self.end_turn_button.draw(self.screen)
                
                # Draw cards (simplified - in a real game you'd have proper card objects)
                if hasattr(self.current_player, 'hand') and self.current_player.hand:
                    card_width = 150
                    card_height = 200
                    start_x = (SCREEN_WIDTH - (len(self.current_player.hand) * (card_width + 10))) // 2
                    
                    for i, card in enumerate(self.current_player.hand):
                        card_display = CardDisplay(start_x + i * (card_width + 10), 
                                                 SCREEN_HEIGHT - card_height - 20, 
                                                 card)
                        card_display.draw(self.screen)
            
            # Draw monster turn info
            if self.game_state == "monster_turn":
                # Could add animation or more visual feedback for monster actions
                pass
                
        elif self.game_state == "game_over":
            # Draw game over message
            self.draw_text(self.message, LARGE_FONT, BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, centered=True)
            # Add restart button if desired
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(FPS)

# Main function
if __name__ == "__main__":
    game = Game()
    game.run()