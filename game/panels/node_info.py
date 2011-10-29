from __future__ import division

import math

import pygame

from engine.render import controls

row_height = 22
header_size = 19
row_size = 17

class NodeInfo (controls.Panel):
    always_redraw = True
    
    def __init__(self, network, size, position, priority=0, fill_colour=(0,0,0), text_colour=(255, 255, 255), selected_colour=(50, 50, 50)):
        super(NodeInfo, self).__init__(position, size, priority)
        
        self.network = network
        
        self.fill_colour = fill_colour
        self.text_colour = text_colour
        self.selected_colour = selected_colour
        
        self.menu = []
        
        self.selected = -1
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        if self.network == None:
            return
        
        if self.network.selected_node < 0:
            return
        
        the_node = self.network.nodes[self.network.selected_node]
        
        controls.draw_text(self._image, "%s [%s]" % (the_node.name, self.network.selected_node),
            (15, 5), self.text_colour, size=22)
        
        controls.draw_text(self._image, "Program", (5, row_height + 5), self.text_colour, size=header_size)
        controls.draw_text(self._image, "Version", (170, row_height + 5), self.text_colour, size=header_size)
        
        keys = list(the_node.programs.keys())
        keys.sort()
        
        for i, prog in enumerate(keys):
            ver = the_node.programs[prog]
            
            if i == self.selected:
                self._image.fill(self.selected_colour, pygame.Rect(0, (i+2) * row_height + 5, self.rect.width, row_height))
            
            controls.draw_text(self._image, prog, (5, 5 + row_height*2 + i*row_height), self.text_colour, size=row_size)
            controls.draw_text(self._image, str(float(ver)), (170, 5 + row_height*2 + i*row_height), self.text_colour, size=row_size)
    
    def handle_mouseup(self, event):
        self.selected = -1
        if self.network == None:
            return
        
        if self.network.selected_node < 0:
            return
        
        the_node = self.network.nodes[self.network.selected_node]
        
        relative_pos = (
            event.pos[0] - self.rect.left,
            event.pos[1] - self.rect.top,
        )
        
        row = int(math.floor(relative_pos[1] / row_height)) - 1
        row -= 1
        
        # Clicked header
        if row < 0:
            return
        
        key_list = list(the_node.programs.keys())
        key_list.sort()
        
        # Clicked too far down
        if row >= len(key_list):
            return
        
        self.selected = row
        
        print("Need to show app window for %s" % key_list[row])
            



