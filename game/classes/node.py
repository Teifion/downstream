
class Node (object):
    def __init__(self, data=None):
        super(Node, self).__init__()
        
        self.position = data['position']
        self.owner = data['owner']
        
        self.connections = set()
        
        self.software = {}
        self.jobs = {}
    
