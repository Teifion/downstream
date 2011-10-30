from engine.render import controls

class Application (object):
    """An application is passed job data and spits out a job class with some
    custom functions dynamically created by the Application"""
    
    def __init__(self, app_type, version=1, **app_data):
        super(Application, self).__init__()
        
        self.app_type   = app_type
        self.version    = version
        self.data       = app_data
    
    def launch_builder(self, *args):
        """This function is designed to return an app launch menu the app
        launch menu will be added to the controls of the game screen and
        when the menu is used the launcher will kill itself and launch this
        application"""
        
        raise Exception("Not implemented")
    
    def launch(self):
        """Creates a job which can then run"""
        
        raise Exception("Not implemented")
    
    def vulnerabilities(self):
        return {}

