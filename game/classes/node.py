from game.classes import user

class Node (object):
    def __init__(self, data=None):
        super(Node, self).__init__()
        
        self.name       = data.get("name", "NoName")
        
        self.position   = data['position']
        self.owner      = data['owner']
        self.cpu_power  = data['cpu_power']
        self.users      = {}
        
        # Add root user
        self.add_user("root", data['password'])
        
        # Nodes that can connect to this one
        self.connections = set()
        
        self.programs = {}# Dict of the programs this node has
        self.jobs = []# ID list of the jobs this node is running
        
        if "software" in data:
            for name, version in data['software'].items():
                self.programs[name] = version
    
    def add_user(self, name, password):
        u = user.User(name, password)
        
        self.users[name] = u
    
