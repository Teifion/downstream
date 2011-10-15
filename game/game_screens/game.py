import pygame

from engine.render import screen, panels

class Game (screen.FullScreen):
    def __init__(self, downstream_game):
        super(Game, self).__init__(downstream_game)
        
        self.controls["network_map"] = panels.InfoBox(downstream_game,
            size = (500, 500),
            position = (300, 300),
            fill_colour = (0,0,0),
            text_colour = (255, 255, 255)
        )
        self.controls["network_map"].always_changed = True
    
    def update(self):
        pass

