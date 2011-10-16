from engine.render import core

from game.game_screens import main_menu, game

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
        self.screens['Game'] = game.Game
        
        self.set_screen('Main menu')
        # self.current_screen.begin_transition("Fade to black", callback=self.new_game, trans_kwargs={"total_frames":30})

    def new_game(self, file_path=""):
        self.set_screen('Game')
        
        self.current_screen.name = "Downstream"

