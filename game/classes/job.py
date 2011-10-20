from __future__ import division

class Job (object):
    """A more accurate name would be process but I want to ensure
    there's no future mixup with the Process from the Multiprocessing
    module."""
    
    short_name = "jbclas"
    full_name = "Job class"
    
    def __init__(self, app_name, version, owner):
        super(Job, self).__init__()
        
        self.progress = 0
        self.max_progress = 1
    
    def get_progress(self):
        return (self.max_progress / self.progress) * 100
    
    



