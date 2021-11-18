class Settings:
    #a class to store the settings for the game 
    #controls game's appearance 
    def __init__(self):
        #initialize the game settings 
        #screen settings 
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #ship settings
        #each key press = 1.5 pixels movement
        self.ship_speed = 1.5 
        # number of ships the player starts with 
        self.ship_limit = 3
        
        #bullet settings 
        #creating a dark grey bullet with width 3px and height 15px 
        self.bullet_speed = 1.5
        self.bullet_width = 10
        self.bullet_height = 15
        #drak grey color 
        self.bullet_color = (60, 60, 60)
        #throw only 3 bullets at a time 
        self.bullets_allowed = 5
        
        #Alien settings 
        self.alien_speed = 1.0 
        self.fleet_drop_speed  = 10 
        # fleet_Direction of: 1 represents right && -1 represents left 
        self.fleet_direction = 1 
        
        
        
        