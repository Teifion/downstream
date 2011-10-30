from __future__ import division

import math

import pygame

from engine.render import controls

row_height = 22
header_size = 19
row_size = 17

class Launcher (controls.Panel):
    always_redraw = True
    accepts_mouseup = True
    
    def __init__(self, size, position, priority=0,
        fill_colour=(0,0,0), text_colour=(255, 255, 255)):
        
        super(Launcher, self).__init__(position, size, priority)
        
        self.fill_colour = fill_colour
        self.text_colour = text_colour
        
        self.options = []
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        i = 0
        for row_text, callback in self.options:
            controls.draw_text(self._image, str(row_text),
                (5, 5 + i*row_height), self.text_colour, size=row_size)
    
    def handle_mouseup(self, event):
        relative_pos = (
            event.pos[0] - self.rect.left,
            event.pos[1] - self.rect.top,
        )
        
        row = int(math.floor(relative_pos[1] / row_height)) - 1
        
        self.launch(row)
    
    def launch(self, option_id):
        text, callback = self.options[option_id]
        
        callback()

