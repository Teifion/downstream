from game.classes import node

class Network (object):
    def __init__(self, data=None):
        super(Network, self).__init__()
        
        self.nodes          = {}
        self.connections    = set()
        
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
            
