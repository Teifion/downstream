import collections
import json

import pygame

from engine.render import screen

from game.classes import network, software, network_map, job_list


class GameScreen (screen.Screen):
    def __init__(self, downstream_game):
        super(GameScreen, self).__init__(downstream_game,
            dimensions=downstream_game.screen_size,
            fullscreen=downstream_game.fullscreen
        )
        
        self.background = (0,0,0)
        
        self.network = None
        
        self.controls["network_map"] = network_map.NetworkMap(
            size = (300, 300),
            position = (10, 10),
            network = self.network
        )
        
        self.controls["job_list"] = job_list.JobList(job_dict = {},
            size = (300, 490),
            position = (10, 320),
            fill_colour = (50,250,50),
            text_colour = (255, 255, 255)
        )
    
    def update(self):
        pass
    
    def load_game(self, file_path):
        with open(file_path) as f:
            data = json.loads(f.read())
        
        # Load network
        self.network = network.Network(data['network'])
        self.network.load_software("data/game_data.json")
        self.controls['network_map'].network = self.network
        