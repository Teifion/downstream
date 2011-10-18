import pygame

from game import application

class NetworkMap (application.Application):
    def __init__(self, size, position, network, priority=0):
        super(NetworkMap, self).__init__(position, size, priority)
        
        self.network = network
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill((255, 255, 255), pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        print(self.rect)
    

