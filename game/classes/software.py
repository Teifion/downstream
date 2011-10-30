import json
import re

from game.apps import cracker

app_lookup = {
    "dict_cracker": cracker.Cracker
}

matcher = re.compile(r"launch\(\) takes exactly [0-9]* arguments \([0-9]* given\)")

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
    
    def launch_app(self, network, owner, parent_node, target_node, app_name, version=1):
        the_app = self.apps[app_name]
        
        try:
            the_job = the_app.launch(network, owner, version)
        except Exception as e:
            if matcher.search(e.message):
                return the_app.launch_builder(network, owner, parent_node, target_node, app_name, version), False
            raise
        
        return the_job, True

