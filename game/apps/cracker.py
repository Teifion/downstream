from game.classes import application, job

class Cracker (application.Application):
    def __init__(self, **app_data):
        super(Cracker, self).__init__(app_type="cracker", **app_data)
    
    def _cpu_cost(self, version):
        pass
    
    def launch(self, owner, version):
        j = job.Job(
            owner       = owner,
            version     = version,
            short_name  = self.data['short_name'],
            full_name   = self.data['full_name'],
        )
        
        # Override the job's _cycle function
        

