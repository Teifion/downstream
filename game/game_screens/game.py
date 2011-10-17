import collections

import pygame

from engine.render import screen, panels

class Game (screen.Screen):
    def __init__(self, downstream_game):
        super(Game, self).__init__(downstream_game,
            dimensions=downstream_game.screen_size,
            fullscreen=downstream_game.fullscreen
        )
        
        self.applications = []
        
        self.background = (0,0,0)
        
        self.controls["network_map"] = panels.InfoBox(downstream_game,
            size = (300, 200),
            position = (10, 10),
            fill_colour = (50,50,50),
            text_colour = (255, 255, 255)
        )
        
        self.controls["job_list"] = panels.InfoBox(downstream_game,
            size = (300, 490),
            position = (10, 220),
            fill_colour = (50,250,50),
            text_colour = (255, 255, 255)
        )
    
    def update(self):
        pass
    
    