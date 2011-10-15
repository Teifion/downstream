from __future__ import division

import math

import pygame
from pygame.locals import *

from engine.render import controls

# Used to draw a grid of information much like the build
# menus from TA or C&C
class TabularMenu (controls.Panel):
    accepts_keyup = True
    
    def __init__(self, engine, position, size, grid_size):
        super(TabularMenu, self).__init__(position, size)
        
        self.screen     = screen
        self.grid_size  = grid_size
        
        self.position.topleft = position
        self.key_map = {}
        
        self._build_list = None
        
        """
        Buttons is a list of tuples: (image_name, callback, args)
        """
        self.buttons = []
    
    def draw(self):
        self._image = pygame.Surface(self.size)
        self._image.fill((100, 100, 100), pygame.Rect(0, 0, self.size[0], self.size[1]))
        
        font = pygame.font.SysFont(None, 30)
        col_count = math.floor(self.size[0]/self.grid_size[0])
        
        col, row = 0, 0
        for actor_name, image_name, queue_length in self.buttons:
            img = self.engine.images[image_name]
            
            self._image.blit(img.get(), pygame.Rect(
                col * self.grid_size[0], row * self.grid_size[1],
                self.grid_size[0], self.grid_size[1],
            ))
            
            # Print the queue size if needed
            if queue_length > 0:
                textobj = font.render(str(queue_length), 1, (0,0,0))
                textrect = textobj.get_rect()
                textrect.topleft = col * self.grid_size[0] + 5, row * self.grid_size[1] + 3
                self._image.blit(textobj, textrect)
            
            col += 1
            if col >= col_count:
                col = 0
                row += 1
        
        self.position.size = self.size
        self.changed = False
    
    def update_queue_sizes(self, button=None):
        if type(button) in (tuple, list):
            raise Exception("No handler to reference a specific button")
        
        elif button != None:
            raise Exception("No handler to reference a specific actor item")
        
        build_queues = {}
        for a in self.screen.selected_actors:
            for b in a.build_queue:
                if b not in build_queues:
                    build_queues[b] = 0
                
                build_queues[b] += 1
        
        for i in range(len(self.buttons)):
            if self.buttons[i][0] in build_queues:
                self.buttons[i][2] = build_queues[self.buttons[i][0]]
        
        self.changed = True
    
    def build_from_actor_list(self):
        """
        Takes a build dict and a list of actors, it then populates itself based
        on what can be built.
        """
        buttons = []
        
        # First build a list of all the flags
        flags = []
        
        # Build a list of all the things currently in the build queues
        build_queues = {}
        for a in self.screen.selected_actors:
            if a.team != self.screen.player_team: continue
            
            flags.extend(a.flags)
            
            for b in a.build_queue:
                if b not in build_queues:
                    build_queues[b] = 0
                
                build_queues[b] += 1
        
        flags = set(flags)
        
        # Now get a list of what can be built
        for f in flags:
            if f in self.screen.build_lists:
                for a in self.screen.build_lists[f]:
                    if a in self.screen.actor_types:
                        img_name = self.screen.actor_types[a]['menu_image']
                    else:
                        print(a, list(self.screen.actor_types.keys()))
                        raise Exception("No handler for %s" % a)
                    
                    buttons.append([a, img_name, build_queues.get(a, 0)])
        
        self.buttons = buttons
        self.changed = True
    
    def handle_keyup(self, event):
        print(event)
    
    def handle_mouseup(self, event, drag=False):
        # It's simply a timing error
        if self.screen.selected_actors == []:
            return
        
        relative_pos = (event.pos[0] - self.position.left, event.pos[1] - self.position.top)
        
        col = math.floor(relative_pos[0]/self.grid_size[0])
        row = math.floor(relative_pos[1]/self.grid_size[1])
        col_count = int(math.floor(self.size[0]/self.grid_size[0]))
        
        index = int((col_count * row) + col)
        
        # No button there? Ignore the click but they clicked the menu
        # so we don't want to pass this back to the screen
        if index >= len(self.buttons):
            return True
        
        # Get the information for the button
        item_name, item_image, queue_length = self.buttons[index]
        
        # What are we looking at?
        print(item_name, item_image, queue_length)
        raise Exception("What now?")
        
        return True

# Used to display text upon a blank background, it's got somewhat
# more functionality than the standard textbox control
class InfoBox (controls.Panel):
    def __init__(self, engine, position, size, fill_colour = (0, 0, 0), text_colour = (255, 255, 255)):
        super(InfoBox, self).__init__(position, size)
        
        self.fill_colour        = fill_colour
        self.text_colour        = text_colour
        
        self.texts = []
    
    def add_text(self, obj, attribute, key=None, position=(0,0), colour=None, prefix="", suffix="", typecast="int"):
        if colour == None: colour = self.text_colour
        
        self.texts.append({
            "obj":          obj,
            "attribute":    attribute,
            "key":          key,
            "position":     position,
            "colour":       colour,
            "prefix":       prefix,
            "suffix":       suffix,
            "typecast":     typecast,
        })  
        
    
    def draw(self):
        self._image = pygame.Surface(self.rect.size)
        self._image.fill(self.fill_colour, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        
        font = pygame.font.SysFont("Helvetica", 16)
        
        for t in self.texts:
            if t['key'] == None:
                v = getattr(t['obj'], t['attribute'])
            else:
                v = getattr(t['obj'], t['attribute'])[t['key']]
            
            if t['typecast'] == "int":
                v = int(v)
            else:
                raise Exception("No handler for typecast type of '%s'" % t['typecast'])
            
            text = "%s%s%s" % (t['prefix'], v, t['suffix'])
            textobj = font.render(text, 1, t['colour'])
            textrect = textobj.get_rect()
            textrect.topleft = t['position']
            
            self._image.blit(textobj, textrect)
        
    def draw_text(self, text, surface, x, y, colour=(0,0,0), font_name="Helvetica", font_size=20):
        font = pygame.font.SysFont(font_name, font_size)
        
        textobj = font.render(text, 1, colour)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    # Not expected to respond to mouse events
    def handle_mouseup(self, event, drag=False):
        pass

