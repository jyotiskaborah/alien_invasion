import sys
from time import sleep
from pathlib import Path

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from botton import Botton
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()


        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create a instance to store game statistics
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = False
        self.game_paused = False
        self.play_botton = Botton(self, "Play")
        self.resume_botton = Botton(self, "Resume")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.game_active and not self.game_paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
         """Watch for mouse and keyboard events."""
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_botton(mouse_pos)
    
    def save_data(self):
        path = Path('data/highest_score')
        path.write_text(str(self.stats.high_score))

    
    def _check_play_botton(self, mouse_pos):
        """Starts the new game when player click Play botton"""
        botton_clicked = self.play_botton.rect.collidepoint(mouse_pos)
        if botton_clicked and not self.game_active:
            self._start_game()
    
    def _check_resume_botton(self, mouse_pos):
        """Resume the game when payer click Resume"""
        botton_clicked = self.resume_botton.rect.collidepoint(mouse_pos)
        if botton_clicked and self.game_active:
            self.game_paused = not self.game_paused


            
    
    def _start_game(self):
        # reset stats
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ship()
        self.settings.initialize_dynamic_settings()
        self.game_active = True

        # Get rid of any remaining bullets and aliens.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Make cursor invisible while playing
        pygame.mouse.set_visible(False)



            
    def _check_keydown_events(self, event):
        """Response to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.game_paused = not self.game_paused

    def _check_keyup_events(self, event):
        """Response to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update bullets positions and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that disappear from the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """Check if any bullet hits alien. if hits disappear alien and bullet"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_highest_score()
        if not self.aliens:
            # Destroy existing bullet and create new freet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level +=1
            self.sb.prep_level()
    
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien first
        # Spacing between aliens is one alien width and one alien height.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height

        while current_y < self.settings.screen_height - 3 * alien_height:
            while current_x < self.settings.screen_width - 2 * alien_width:
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    
    def _create_alien(self, x_position, y_position):
        """Create an alien on given position and add to fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropiatly when fleet reach edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def _update_aliens(self):
        """check if any alien on edge and Move the whole fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        """Responds to the ship hit by alien"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ship()
            # Delete remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # reposition ship and create new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check if any alien reach the bottom of screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this same as ship hit.
                self._ship_hit()
                break


    

    def _update_screen(self):
        """Update image on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_botton.draw_botton()
        if self.game_paused:
            self.resume_botton.draw_botton()
        # Make most recently drawn screen visible.
        pygame.display.flip()

            


if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
