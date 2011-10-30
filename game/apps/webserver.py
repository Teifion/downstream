from game.classes import application, job, user

class WebServer (application.Application):
    def __init__(self, **app_data):
        super(WebServer, self).__init__(app_type="webserver", **app_data)
    
    def launch(self, network, owner, version):
        j = job.Job(
            owner           = owner,
            version         = version,
            short_name      = self.data['short_name'],
            full_name       = self.data['full_name'],
            max_progress    = -1
        )
        
        def _cycle(*args, **kwargs):
            pass
        
        j._cycle    = _cycle
        
        return j
    
    def vulnerabilities(self):
        return {}

