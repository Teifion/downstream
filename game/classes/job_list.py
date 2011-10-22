import pygame

from engine.render import controls

class JobList (controls.Panel):
    always_redraw = True
    
    def __init__(self, job_dict, size, position, priority=0, fill_colour=(0,0,0), text_colour=(255, 255, 255)):
        super(JobList, self).__init__(position, size, priority)
        
        self.jobs = job_dict
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill((0, 0, 0), pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        i = -1
        for job_id, the_job in self.jobs.items():
            i += 1
            print(dir(the_job))
            
            controls.draw_text(self._image, job_id, (5, 5+i*20), (255, 255, 255))
    
