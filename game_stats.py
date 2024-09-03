class GameStats:
    """Track all game statistics"""
    def __init__(self, ai_games):
        """Initialise Statistics"""
        self.settings = ai_games.settings
        self.reset_stats()

    def reset_stats(self):
        """Reset stats that can change during game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
