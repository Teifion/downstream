from game.classes import user

class Node (object):
    def __init__(self, data=None):
        super(Node, self).__init__()
        
        self.node_id    = data['node_id']
        self.name       = data.get("name", "NoName")
        
        self.position   = data['position']
        self.owner      = data['owner']
        self.admin_type = data['admin']
        self.cpu_power  = data['cpu_power']
        self.users      = {}
        
        # Add root user
        self.add_user("root", data['password'])
        
        # Nodes that can connect to this one
        self.connections = set()
        
        self.programs = {}# Dict of the programs this node has
        self.jobs = []# ID list of the jobs this node is running
        self.services = {}
        
        self.running_services = {}
        
        if "software" in data:
            for name, version in data['software'].items():
                self.programs[name] = version
        
        if "services" in data:
            for name, version in data['services'].items():
                self.programs[name] = version
                self.services[name] = version
    
    def add_user(self, name, password):
        u = user.User(name, password)
        
        self.users[name] = u
    
    def run_admin(self, network):
        """The machine admin does a sweep and tries to remove hacked
        services etc etc."""
        
        for name, version in self.services.items():
            if name not in self.running_services:
                jid = network.launch_app(
                    owner_id    = self.owner,
                    parent_node = self.node_id,
                    target_node = self.node_id,
                    app_name    = name,
                )
                
                self.running_services[name] = jid

