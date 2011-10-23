from __future__ import division

import pygame

from engine.render import controls

node_size = 20

player_colours = {
    "player_0": ((0, 0, 100), (100, 100, 255)),
    "player_1": ((100, 0, 0), (255, 100, 100)),
    "neutral":  ((100, 100, 100), (255, 255, 255)),
}

class NetworkMap (controls.Panel):
    always_redraw = True
    
    def __init__(self, size, position, network, priority=0):
        super(NetworkMap, self).__init__(position, size, priority)
        
        self.network = network
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill((0, 0, 0), pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        if self.network == None:
            return
        
        # Connections
        for n1, n2 in self.network.connections:
            pygame.draw.line(self._image, (255, 255, 255), self.network.nodes[n1].position, self.network.nodes[n2].position)
        
        # Draw nodes first
        for nid, node in self.network.nodes.items():
            colour = player_colours[node.owner]
            
            node_rect = pygame.Rect(
                node.position[0]-node_size/2,
                node.position[1]-node_size/2,
                node_size,
                node_size,
            )
            self._image.fill(colour[0], node_rect)
            pygame.draw.rect(self._image, colour[1], node_rect, 1)
            
    def handle_mouseup(self, event):
        x, y = (
            event.pos[0] - self.rect.left,
            event.pos[1] - self.rect.top,
        )
        
        for nid, node in self.network.nodes.items():
            left    = node.position[0] - node_size/2
            right   = node.position[0] + node_size/2
            
            if left <= x <= right:
                top     = node.position[1] - node_size/2
                bottom  = node.position[1] + node_size/2
                
                if top <= y <= bottom:
                    return self.click_node(nid)
        
        self.network.selected_node = -1
        
    def click_node(self, n):
        self.network.selected_node = n
        
    

