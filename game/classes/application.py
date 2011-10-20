from engine.render import controls

class Application (object):
    def __init__(self, app_type, version=1, **job_data):
        super(Application, self).__init__()
        
        self.app_type = app_type
        self.version = version
        self.job_data = job_data
