import pygame

from engine.render import core

from game.game_screens import main_menu, game_screen

class Downstream (core.EngineV3):
    name = "Downstream"
    
    fps = 30
    
    screen_size = [1280, 720]
    fullscreen = False
    
    def __init__(self):
        super(Downstream, self).__init__()
        
        self.images = {}
    
    def startup(self):
        super(Downstream, self).startup()
        
        self.screens['Main menu'] = main_menu.MainMenu(self)
        self.screens['Game'] = game_screen.GameScreen
        
        self.set_screen('Main menu')
        # self.current_screen.begin_transition("Fade to black", callback=self.new_game, trans_kwargs={"total_frames":30})
        self.new_game()

    def new_game(self, file_path=""):
        self.set_screen('Game')
        
        cs = self.current_screen
        cs.player = "player_0"
        
        cs.name = "Downstream"
        cs.load_game("data/dummy.json")
        
        # cs.network.launch_app(owner_id=0, node_id=0, app_name="dict_cracker",
        #     target_password=cs.network.nodes[0].users["root"].password)
        
        # Fake some clicks
        cs._handle_mouseup(pygame.event.Event(6, button=1, pos=(57, 157)))# Click our computer node
        cs._last_mouseup[1] = 0
        
        cs._handle_mouseup(pygame.event.Event(6, button=1, pos=(62, 383)))# Select dict cracker
        cs._last_mouseup[1] = 0
        
        pygame.mouse.set_pos(111, 211)
        cs._handle_mouseup(pygame.event.Event(6, button=1, pos=(111, 211)))# Target a node
        cs._last_mouseup[1] = 0
