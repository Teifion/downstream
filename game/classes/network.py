import random

import pygame

from game.classes import node, software
from game.panels import launcher

class Network (object):
    def __init__(self, screen, data=None, software=None):
        super(Network, self).__init__()
        
        self.players        = {}
        
        self.nodes          = {}
        self.connections    = set()
        self.jobs           = {}
        self.software       = software
        
        self.selected_node  = -1
        self.screen = screen
        
        if data != None:
            self.load_from_data(data)
    
    def load_from_data(self, data):
        self.nodes          = {}
        self.connections    = set()
        
        for node_name, node_data in data['nodes'].items():
            node_data['node_id'] = int(node_name)
            self.nodes[int(node_name)] = node.Node(node_data)
        
        for n1, n2 in data['connections']:
            self.nodes[n1].connections.add(n2)
            self.nodes[n2].connections.add(n1)
            
            self.connections.add((n1, n2))
    
    def load_software(self, file_path):
        self.software = software.Software(file_path)
    
    def launch_app(self, owner_id, parent_node, target_node, app_name, **kwargs):
        # Node handle
        the_node = self.nodes[parent_node]
        
        # Get version
        version = the_node.programs.get(app_name, -1)
        
        # Make sure we have it
        if version < 0:
            raise KeyError("Node[%s] has no program by the name of %s" % (parent_node, app_name))
        
        the_job, is_job = self.software.launch_app(self, owner_id, parent_node, target_node, app_name, version, **kwargs)
        
        if not is_job:
            return self.launch_launcher(the_job)
        
        the_job.node = parent_node
        
        while True:
            # Keep trying till we get a random number not yet used
            jid = random.randint(0, 999999)
            if jid not in self.jobs:
                self.jobs[jid] = the_job
                break
        
        the_node.jobs.append(jid)
        
        return jid
    
    def launch_launcher(self, the_launcher):
        the_launcher.rect.topleft = pygame.mouse.get_pos()
        # the_launcher.rect.topleft = (100, 300)
        
        self.screen.controls['launcher'] = the_launcher
    
    def reachable_nodes(self, owner="", node=-1):
        """Returns a list of node IDs that are reachable from either a single
        node or from the combination of nodes owned by a player."""
        
        if owner != "":
            # Get all the nodes with our owner
            filterfunc = lambda n: n[1].owner == owner
            nodes_to_read_from = [n[0] for n in filter(filterfunc, self.nodes.items())]
        elif node >= 0:
            nodes_to_read_from = [node]
        else:
            raise Exception("No owner or node selected")
        
        found_nodes = set()
        
        for n1, n2 in self.connections:
            if n1 in nodes_to_read_from or n2 in nodes_to_read_from:
                found_nodes.add(n1)
                found_nodes.add(n2)
        
        return found_nodes

