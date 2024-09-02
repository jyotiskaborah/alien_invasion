from typing import Any
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for bullet and properties"""
    def __init__(self, ai_game):
        """Create bullet at ships position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Create a bullet rectangle at (0, 0) and then se correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet position as float
        self.y = float(self.rect.y)


    def update(self):
        """Change the position and go up"""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rectange position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)