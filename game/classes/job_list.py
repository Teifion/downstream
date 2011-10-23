import pygame

from engine.render import controls

class JobList (controls.Panel):
    always_redraw = True
    
    def __init__(self, network, size, position, priority=0, fill_colour=(0,0,0), text_colour=(255, 255, 255)):
        super(JobList, self).__init__(position, size, priority)
        
        self.network = network
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill((0, 0, 0), pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        if self.network == None:
            return
        
        i = -1
        for job_id, the_job in self.network.jobs.items():
            i += 1
            
            controls.draw_text(self._image, str(job_id), (5, 5+i*20), (255, 255, 255))
    
