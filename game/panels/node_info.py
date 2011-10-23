from __future__ import division

import pygame

from engine.render import controls

class NodeInfo (controls.Panel):
    def __init__(self, network, size, position, priority=0, fill_colour=(0,0,0), text_colour=(255, 255, 255)):
        super(NodeInfo, self).__init__(position, size, priority)
        
        self.network = network
        
        self.fill_colour = fill_colour
        self.text_colour = text_colour
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        if self.network.selected_node < 0:
            return
        
        controls.draw_text(self._image, "Job", (5, 5), self.text_colour, size=header_size, bold=True)



