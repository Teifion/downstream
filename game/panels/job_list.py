from __future__ import division

import math

import pygame

from engine.render import controls

row_height = 22
header_size = 19
row_size = 17

class JobList (controls.Panel):
    always_redraw = True
    
    def __init__(self, network, size, position, priority=0, fill_colour=(0,0,0), text_colour=(255, 255, 255)):
        super(JobList, self).__init__(position, size, priority)
        
        self.network = network
        
        self.fill_colour = fill_colour
        self.text_colour = text_colour
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        if self.network == None:
            return
        
        controls.draw_text(self._image, "Job", (5, 5), self.text_colour, size=header_size, bold=True)
        controls.draw_text(self._image, "Node", (70, 5), self.text_colour, size=header_size, bold=True)
        controls.draw_text(self._image, "App", (130, 5), self.text_colour, size=header_size, bold=True)
        controls.draw_text(self._image, "%", (215, 5), self.text_colour, size=header_size, bold=True)
        
        key_list = list(self.network.jobs.keys())
        key_list.sort()
        
        i = 0
        for job_id in key_list:
            the_job = self.network.jobs[job_id]
            i += 1
            
            # Job ID
            controls.draw_text(self._image, str(job_id),
                (5, 5+i*row_height), self.text_colour, size=row_size)
            
            # Node ID
            controls.draw_text(self._image, str(the_job.node),
                (70, 5+i*row_height), self.text_colour, size=row_size)
            
            # App name
            controls.draw_text(self._image, "%s%s" % (the_job.short_name, the_job.version),
                (130, 5+i*row_height), self.text_colour, size=row_size)
            
            # Progress
            controls.draw_text(self._image, "%s%%" % int(the_job.get_progress()),
                (215, 5+i*row_height), self.text_colour, size=row_size)

    def handle_mouseup(self, event):
        relative_pos = (
            event.pos[0] - self.rect.left,
            event.pos[1] - self.rect.top,
        )
        
        row = int(math.floor(relative_pos[1] / row_height)) - 1
        
        # Clicked header
        if row == -1:
            return
        
        key_list = list(self.network.jobs.keys())
        key_list.sort()
        
        # Clicked too far down
        if row >= len(key_list):
            return
        
        print("Need to show app window for %s" % key_list[row])
    
