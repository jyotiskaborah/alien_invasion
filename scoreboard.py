import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Class to create scoreboard information"""
    def __init__(self, ai_game):
        """Initialize components"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    
    def prep_score(self):
        """create an image of the score"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        """Make a image with the highest score"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Make image of current level"""
        level_str = str(self.stats.level)
        self.level_img = self.font.render("Level: "+level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.screen_rect.right -20
        self.level_rect.top = self.score_rect.bottom
    
    def prep_ship(self):
        """Create image to show remaining ships"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    
    def check_highest_score(self):
        """To check if cureent score is high than highest score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    
    def show_score(self):
        """Display the scores, ships and level on the screen"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)




