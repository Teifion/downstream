import collections
import json
import time

import pygame

from engine.render import screen
from engine.libs import screen_lib

from game.classes import network, software, network_map, job_list


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
            size = (300, 490),
            position = (10, 320),
            fill_colour = (50,250,50),
            text_colour = (255, 255, 255),
            network = self.network
        )
        
        self.tick = 0
    
    def update(self):
        if time.time() < self._next_update:
            return
        
        self.tick += 1
        
        for jid, job in self.network.jobs.items():
            job.cycle()
        
        self._next_update = time.time() + self._update_delay
    
    def load_game(self, file_path):
        with open(file_path) as f:
            data = json.loads(f.read())
        
        # Load network
        self.network = network.Network(data['network'])
        self.network.load_software("data/game_data.json")
        self.controls['network_map'].network = self.network
        self.controls['job_list'].network = self.network

