import random

from game.classes import node, software

class Network (object):
    def __init__(self, data=None, software=None):
        super(Network, self).__init__()
        
        self.nodes          = {}
        self.connections    = set()
        self.jobs           = {}
        self.software       = software
        
        if data != None:
            self.load_from_data(data)
    
    def load_from_data(self, data):
        self.nodes          = {}
        self.connections    = set()
        
        for node_name, node_data in data['nodes'].items():
            self.nodes[int(node_name)] = node.Node(node_data)
        
        for n1, n2 in data['connections']:
            self.nodes[n1].connections.add(n2)
            self.nodes[n2].connections.add(n1)
            
            self.connections.add((n1, n2))
    
    def load_software(self, file_path):
        self.software = software.Software(file_path)
    
    def launch_app(self, owner_id, node_id, app_name, **kwargs):
        # Node handle
        the_node = self.nodes[node_id]
        
        # Get version
        version = the_node.programs.get(app_name, -1)
        
        # Make sure we have it
        if version < 0:
            raise KeyError("Node[%s] has no program by the name of %s" % (node_id, app_name))
        
        the_job = self.software.launch_app(owner_id, app_name, version, **kwargs)
        
        while True:
            # Keep trying till we get a random number not yet used
            jid = random.randint(0, 999999)
            if jid not in self.jobs:
                self.jobs[jid] = the_job
                break
        
        the_node.jobs.append(the_job)
