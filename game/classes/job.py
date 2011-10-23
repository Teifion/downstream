from __future__ import division

class Job (object):
    """A more accurate name would be process but I want to ensure
    there's no future mixup with the Process from the Multiprocessing
    module."""
    
    def __init__(self, owner, version=1, short_name="jbclas", full_name="Job class", max_progress=1, max_cpu=1):
        super(Job, self).__init__()
        
        self.progress = 0
        self.max_progress = max_progress
        
        self.owner  = owner
        self.node   = -1
        
        self.short_name = short_name
        self.full_name  = full_name
        self.version    = float(version)
        
        # It's possible that an app cannot run beyond a certain speed
        self.max_cpu = max_cpu
        
        self.is_complete = False
    
    def get_progress(self):
        return (self.progress/self.max_progress) * 100
    
    def _cycle(self, cpu_points = 1):
        raise Exception("Not implemented")
    
    def _complete(self):
        raise Exception("Not implemented")
    
    def cycle(self, cpu_points = 1):
        if self.is_complete: return
        
        self._cycle(cpu_points)
        self.progress += min(cpu_points, self.max_cpu)
        
        if self.progress >= self.max_progress:
            self._complete()
            self.is_complete = True



