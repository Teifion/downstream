from engine.render import controls

class Application (object):
    """An application is passed job data and spits out a job class with some
    custom functions dynamically created by the Application"""
    
    def __init__(self, app_type, version=1, **app_data):
        super(Application, self).__init__()
        
        self.app_type = app_type
        self.version = version
        self.data = app_data

    def launch(self):
        raise Exception("Not implemented")

