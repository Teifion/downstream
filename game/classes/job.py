from __future__ import division

class Job (object):
    """A more accurate name would be process but I want to ensure
    there's no future mixup with the Process from the Multiprocessing
    module."""
    
    def __init__(self, owner, version=1, short_name="jbclas", full_name="Job class"):
        super(Job, self).__init__()
        
        self.progress = 0
        self.max_progress = 1
        
        self.owner = owner
        
        self.short_name = short_name
        self.full_name  = full_name
    
    def get_progress(self):
        return (self.max_progress / self.progress) * 100
    
    def _cycle(self, cpu_points = 1):
        raise Exception("Not implemented")
    
    def _complete(self):
        raise Exception("Not implemented")
    
    def cycle(self, cpu_points = 1):
        self._cycle(cpu_points)
        self.progress += cpu_points
        
        if self.progress >= self.max_progress:
            self._complete()



