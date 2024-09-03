import pygame.font

class Botton():
    """A class to built botton for the game"""
    def __init__(self, ai_game, msg):
        """Initialise the attributes for font and botton"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Set the dimenssion and properties of the botton
        self.width, self.height = 200 , 50
        self.botton_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Built the botton rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center the text to the botton"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.botton_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_botton(self):
        """Draw blank botton and then the text"""
        self.screen.fill(self.botton_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        



