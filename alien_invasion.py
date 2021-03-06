import sys 

# importing sleep function from the time module in py so that we can pause the game for a moment the ship is hit 
from time import sleep 

import pygame

from settings import Settings

from game_stats import GameStats

from ship import Ship

from bullet import Bullet

from alien import Alien 

class AlienInvasion:
    #it's an overall class to maintain all the game assets and behaviour   

    def __init__(self):
        #initialize the game and create game resources 
        pygame.init() 
        self.settings = Settings() 

        #setting the game into full screen 
        self.screen = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN )
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        # create an instance to store game statistics 
        # making this window before defining other game components
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

        #set background color 
        #self.bg_color = (230, 230, 230 )

    def run_game(self):
        #start the main loop for the game 
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            #print(len(self.bullets))
            self._update_aliens()
            self._update_screen()
    
    def _create_fleet(self):
        #create the fleet of aliens 
        #create an alien and calculate the number of aliens in a row 
        #spacing between each alien is equal to one alien width 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        #determine the number of rows of aliens that fit on the screen 
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        #create full fleet of aliens 
        #outer loop calculates the number of rows we require 
        for row_number in range(number_rows):
            #create the first row of aliens
            #loop from 0 to number of aliens which would fit in a single row  
            #the inner loop calculates the number of aliens we require is a single row 
            for alien_number in range(number_aliens_x):
                self._create_aliens(alien_number, row_number)
            
    def _create_aliens(self, alien_number, row_number):
        #create an alien and place it in a row 
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            #alien's x coordinate 
            alien.rect.x = alien.x
            #alien's y coordinate
            alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
            self.aliens.add(alien)
        
    def _check_events(self):
        #respond to key-press and mouse events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                        
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                    
    def _check_keydown_events(self, event):
        #respond to key-presses 
        if event.key == pygame.K_RIGHT:
        #move the ship to the right till the right arrow key pressed 
            self.ship.moving_right = True 
        #move the ship to the left
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #press q to exit/exit the game  
        elif event.key == pygame.K_q:
            sys.exit()
        #pressing space bar will fire the bullets 
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
                        
    def _check_keyup_events(self, event):
        #respond to key-releases 
        #as soon as we stop pressing the right arrow key, the right movement will stop
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
                
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False 
                
    def _fire_bullet(self):
        #craete a new bullet and add it to the bullets group 
        if len(self.bullets) < self.settings.bullets_allowed :
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        #update position of bullets and get rid of old bullets 
        #old bullets = the ones going up and off the screen
        self.bullets.update()
            #get rid of bullets that have dissapeared 
        for bullet in self.bullets.copy() :
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
                
    def _check_bullet_alien_collisions(self):
        # chech if any bullet has hit any alien -> 
        # if so, get rif of the bullet and that particular alien 
        #groupcollide -> checking whether the first 2 parameters are in the same position or not, if they are it means that they ahve collided and returns True in both case ordering the first the parameters to delete themselves 
        #hence destroying that particular bullet and alien 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        # if no alien group is found
        if not self.aliens :
            # destroy existing bullets and create a new fleet 
            self.bullets.empty()
            self._create_fleet()
                    
                    
    def _update_screen(self):
        #redraw the screen during each pass through the loop 
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            #drawing the alien on the screen 
            self.aliens.draw(self.screen)
 
            #make the most recently drawn screen visible  
            pygame.display.flip()
            
    def _update_aliens(self):
        
        # check if the fleet is at the edge -> update the position of all the aliens in the fleet 
        self._check_cleet_edges()
        #update the position of all the aliens on the fleet 
        self.aliens.update()
        
        #look for alien-ship collisions 
        if pygame.sprite.spritecollideany( self.ship, self.aliens ):
            self._ship_hit()
        
    def _check_cleet_edges(self):
        # check whether the aliens have reached the edge/end or not 
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        # drop the entire fleet and change the fleet's direction 
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1 
        
        
    def _ship_hit(self) :
        #respond to ship being hit by an alien 
        
        # decrease ships_left 
        self.stats.ships_left -= 1
        
        # get rid of any remaining aliens or bullets -> deleting 
        self.aliens.empty()
        self.bullets.empty()

        #create a new flwwt and center the fleet 
        self._create_fleet()
        self.ship.center_ship()
        
        # pause 
        sleep(0.5)
        
        
if __name__ == '__main__' :
    #make a game instance and run the game 
    #pygame.init()
    ai = AlienInvasion()
    ai.run_game()  