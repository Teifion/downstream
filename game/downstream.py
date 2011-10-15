from engine.render import core

from game.game_screens import main_menu

class Downstream (core.EngineV3):
    name = "Downstream"
    
    fps = 30
    
    window_width = 1000
    window_height = 1000
    
    def __init__(self):
        super(Downstream, self).__init__()
        
        self.images = {}
    
    def startup(self):
        super(Downstream, self).startup()
        
        self.screens['Main menu'] = main_menu.MainMenu(self)
        
        self.set_screen('Main menu')

    def new_game(self, file_path=""):
        pass
