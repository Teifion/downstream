import collections
import json
import time

import pygame

from engine.render import screen
from engine.libs import screen_lib

from game.classes import network, software, player
from game.panels import network_map, job_list, node_info

class GameScreen (screen.Screen):
    def __init__(self, downstream_game):
        super(GameScreen, self).__init__(downstream_game,
            dimensions=downstream_game.screen_size,
            fullscreen=downstream_game.fullscreen
        )
        
        self._next_update = time.time()
        self._update_delay = screen_lib.set_fps(self, 30)
        
        self.background = (0,0,0)
        
        self.network = None
        
        self.controls["network_map"] = network_map.NetworkMap(
            size = (300, 300),
            position = (10, 10),
            network = self.network
        )
        
        self.controls["job_list"] = job_list.JobList(
            size = (300, downstream_game.screen_size[1] - 20),
            position = (downstream_game.screen_size[0] - 310, 10),
            fill_colour = (50,50,50),
            text_colour = (255, 255, 255),
            network = self.network
        )
        
        self.controls["node_info"] = node_info.NodeInfo(
            size = (300, 390),
            position = (10, 320),
            fill_colour = (50,50,50),
            selected_colour = (50, 50, 100),
            text_colour = (255, 255, 255),
            network = self.network
        )
        
        self.tick = 0
    
    def update(self):
        if time.time() < self._next_update:
            return
        
        self.tick += 1
        
        to_remove = []
        for jid, job in self.network.jobs.items():
            job.cycle()
            
            if job.is_complete:
                to_remove.append(jid)
        
        for r in to_remove:
            del(self.network.jobs[r])
        
        self._next_update = time.time() + self._update_delay
    
    def load_game(self, file_path):
        with open(file_path) as f:
            data = json.loads(f.read())
        
        # Load network
        self.network = network.Network(data['network'])
        self.network.load_software("data/game_data.json")
        
        for k, v in data['players'].items():
            self.network.players[int(k)] = player.Player(int(k), v)
        
        self.controls['network_map'].network = self.network
        self.controls['job_list'].network = self.network
        self.controls['node_info'].network = self.network
        
