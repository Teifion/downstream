import pygame

from game import application

player_colours = {
    "player_0": ((0, 0, 100), (100, 100, 255)),
    "player_1": ((100, 0, 0), (255, 100, 100)),
    "neutral":  ((100, 100, 100), (255, 255, 255)),
}

class NetworkMap (application.Application):
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
                node.position[0]-10,
                node.position[1]-10,
                20,
                20,
            )
            self._image.fill(colour[0], node_rect)
            pygame.draw.rect(self._image, colour[1], node_rect, 1)
            
        
        
    

