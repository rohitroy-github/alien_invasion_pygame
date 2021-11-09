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
        
        #bullet settings 
        #creating a dark grey bullet with width 3px and height 15px 
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        #drak grey color 
        self.bullet_color = (60, 60, 60)
        #throw only 3 bullets at a time 
        self.bullets_allowed = 3
        
        
        