import json

from game.apps import cracker

app_lookup = {
    "dict_cracker": cracker.Cracker
}

class Software (object):
    """Simply something to allow us to lookup the classes and software"""
    def __init__(self, load_path=""):
        super(Software, self).__init__()
        
        self.apps = {}
        
        if load_path != "":
            self.load_apps(load_path)
    
    def load_apps(self, file_path):
        with open(file_path) as f:
            data = json.loads(f.read())
        
        # Load apps
        for k, v in data['apps'].items():
            self.add_app(k, v)
    
    def add_app(self, app_name, app_data):
        app_class = app_lookup[app_name]
        
        self.apps[app_name] = app_class(**app_data)
    
    def launch_app(self, owner, app_name, version=1, **kwargs):
        the_app = self.apps[app_name]
        the_job = the_app.launch(owner, version, **kwargs)
        
        return the_job