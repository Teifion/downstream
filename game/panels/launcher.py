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
        if self.kill: return
        
        self._image = pygame.Surface(self.rect.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        i = -1
        for row_text, callback in self.options:
            i += 1
            controls.draw_text(self._image, str(row_text),
                (5, 5 + i*row_height), self.text_colour, size=row_size)
        
        # Close window button
        self._image.fill((200, 0, 0), pygame.Rect(self.rect.width-25, 0, 25, 25))
        pygame.draw.aaline(self._image, (255, 100, 100), (self.rect.width - 23, 2), (self.rect.width - 2, 23))
        pygame.draw.aaline(self._image, (255, 100, 100), (self.rect.width - 23, 23), (self.rect.width - 2, 2))
    
    def handle_mouseup(self, event):
        relative_pos = (
            event.pos[0] - self.rect.left,
            event.pos[1] - self.rect.top,
        )
        
        if relative_pos[0] > self.rect.width - 25:
            if relative_pos[1] < 25:
                self.kill = True
                return
        
        row = int(math.floor(relative_pos[1] / row_height)) - 1
        
        self.launch(row)
        self.kill = True
    
    def launch(self, option_id):
        text, callback = self.options[option_id]
        
        callback()

