class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Inisialize the game static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Alien Settings
        self.fleet_drop_speed = 10



        # How quickly the game speed up
        self.speedup_scale = 1.1
        # Score increses in each level
        self.scoring_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """"Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        # scoring settings
        self.alien_points = 50
        # Fleet direction 1 represet right, -1 left
        self.fleet_direction = 1

    def increase_speed(self):
        """increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # increase the score with speed
        self.alien_points = int(self.alien_points * self.scoring_scale)


        

