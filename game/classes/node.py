
class Node (object):
    def __init__(self, data=None):
        super(Node, self).__init__()
        
        self.position = data['position']
        self.owner = data['owner']
        
        # Nodes that can connect to this one
        self.connections = set()
        
        self.programs = {}# Dict of the programs this node has
        self.jobs = []# ID list of the jobs this node is running
        
        if "software" in data:
            for name, version in data['software'].items():
                self.programs[name] = version
                
