from __future__ import division

import time

import pygame
from pygame.locals import *

from engine.libs import screen_lib

class Screen (object):
    # When set to true the screen has to regulate the FPS itself
    self_regulate = False
    
    fullscreen = False
    
    facings = 360/4# The number of different angles we'll draw
    
    def __init__(self, engine, dimensions):
        super(Screen, self).__init__()
        
        self.actors = {}
        self.controls = {}
        self.buttons = []
        
        self.name = ""
        self.engine = engine
        self.size = dimensions
        
        self.image_cache = {}
        
        self.mouse_is_down = False
        self.keys_down = {}
        self.scroll_x, self.scroll_y = 0, 0
        self.mouse = [0,0]
        self.mouse_down_at = [0,0]
        
        self.engine = None
        self.background_image = None
        self.background = (200, 200, 200)# Default to a grey background
        
        if self.fullscreen:
            # TODO work out if it's okay to use the HWSURFACE flag
            # or if I need to stick wih FULLSCREEN
            self.surf = pygame.display.set_mode(dimensions, FULLSCREEN)
        else:
            self.surf = pygame.Surface(dimensions)
        
        self._last_mouseup = [None, -1]
        self._double_click_interval = 0.25
    
    def add_button(self, b):
        self.buttons.append(b)
    
    def update(self):
        """
        This is called every execution loop to allow the game to do 'stuff'
        """
        raise Exception("{0}.update() is not implemented".format(self.__class__))
    
    def get_rotated_image(self, core_image_name, frame, rotation):
        rounded_facing = screen_lib.get_facing_angle(
            rotation, self.facings
        )
        
        # Build name
        img_name = "%s_%s_%s" % (
            core_image_name,
            self.engine.images[core_image_name].real_frame(frame),
            rounded_facing,
        )
        
        # Cache miss?
        if img_name not in self.image_cache:
            self.image_cache[img_name] = screen_lib.make_rotated_image(
                image = self.engine.images[core_image_name].get(frame),
                angle = rounded_facing,
            )
        
        return self.image_cache[img_name]
    
    def redraw(self):
        """Basic screens do not have scrolling capabilities
        you'd need to use a subclass for that"""
        surf = self.engine.display
        
        # CODE NOT YET TESTED
        # Actors
        for i, a in self.actors.items():
            a.frame += 1
            
            if 0 < a.position[0] < self.size[0]:
                if 0 < a.position[1] < self.size[1]:
                    actor_img = self.get_rotated_image(a.image, a.frame, rounded_facing)
                    
                    r = pygame.Rect(actor_img.get_rect())
                    r.left = a.pos[0] + self.draw_margin[0] - r.width/2
                    r.top = a.pos[1] + self.draw_margin[1] - r.height/2
                    
                    surf.blit(actor_img, r)
        
        # Panels, unlike actors we draw all of them unless they
        # tell us not to
        for i, c in self.controls.items():
            if c.visible:
                surf.blit(*c.image())
        
        pygame.display.flip()
    
    def update_window(self):
        """Used when we've changed screen or want to simply redraw everything"""
        if type(self.background) == tuple or type(self.background) == list:
            self.display.fill(self.background)
        else:
            self.background = self.background_image.copy()
            self.display.blit(self.background, pygame.Rect(0, 0, self.size[0], self.size[1]))
        
        pygame.display.flip()
        self.redraw()
    
    
    # Event handlers
    # Internal version allows us to sub-class without requiring a super call
    # makes the subclass cleaner
    def _handle_active(self, event):
        self.handle_active(event)
    
    def handle_active(self, event):
        pass
    
    def _handle_keydown(self, event):
        self.keys_down[event.key] = time.time()
        self.test_for_keyboard_commands()
        self.handle_keydown(event)
    
    def handle_keydown(self, event):
        pass
    
    def _handle_keyup(self, event):
        if event.key in self.keys_down:
            del(self.keys_down[event.key])
        self.handle_keyup(event)
    
    def handle_keyup(self, event):
        pass
    
    def _handle_keyhold(self):
        if len(self.keys_down) > 0:
            self.handle_keyhold()

    def handle_keyhold(self):
        pass
    
    def _handle_mousedown(self, event):
        self.mouse_down_at = (event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y)
        
        for b in self.buttons:
            if b.button_down != None:
                if b.contains(event.pos):
                    b.button_down(*b.button_down_args, **b.button_down_kwargs)
        
        self.mouse_is_down = True
        self.handle_mousedown(event)
    
    def handle_mousedown(self, event):
        pass
    
    def _handle_mouseup(self, event):
        if time.time() <= self._last_mouseup[1] + self._double_click_interval:
            return self._handle_doubleclick(self._last_mouseup[0], event)
        
        self._last_mouseup = [event, time.time()]
        real_mouse_pos = (event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y)
        
        for b in self.buttons:
            if b.button_up != None:
                if b.contains(event.pos):
                    try:
                        b.button_up(*b.button_up_args, **b.button_up_kwargs)
                    except Exception as e:
                        print("Func: %s" % b.button_up)
                        print("Args: %s" % b.button_up_args)
                        print("Kwargs: %s" % b.button_up_kwargs)
                        raise
        
        self.mouse_is_down = False
        if real_mouse_pos == self.mouse_down_at:
            self.handle_mouseup(event, drag=False)
        else:
            self._handle_mousedragup(event)
            self.handle_mouseup(event, drag=True)
    
    def handle_mouseup(self, event, drag=False):
        pass
    
    def _handle_doubleclick(self, first_click, second_click):
        self.handle_doubleclick(first_click, second_click)
    
    def handle_doubleclick(self, first_click, second_click):
        pass
    
    def _handle_mousemotion(self, event):
        self.mouse = event.pos
        self.handle_mousemotion(event)
        
        if self.mouse_is_down:
            self._handle_mousedrag(event)
    
    def handle_mousemotion(self, event):
        pass
    
    def _handle_mousedrag(self, event):
        if self.mouse_down_at == None:
            return self.handle_mousedrag(event, None)
        
        real_mouse_pos = (event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y)
        
        drag_rect = (
            min(self.mouse_down_at[0], real_mouse_pos[0]),
            min(self.mouse_down_at[1], real_mouse_pos[1]),
            max(self.mouse_down_at[0], real_mouse_pos[0]),
            max(self.mouse_down_at[1], real_mouse_pos[1]),
        )
        self.handle_mousedrag(event, drag_rect)
    
    def handle_mousedrag(self, event, drag_rect):
        pass
    
    def _handle_mousedragup(self, event):
        if self.mouse_down_at == None:
            return self.handle_mousedragup(event, None)
            
        real_mouse_pos = (event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y)
        
        drag_rect = (
            min(self.mouse_down_at[0], real_mouse_pos[0]),
            min(self.mouse_down_at[1], real_mouse_pos[1]),
            max(self.mouse_down_at[0], real_mouse_pos[0]),
            max(self.mouse_down_at[1], real_mouse_pos[1]),
        )
        self.handle_mousedragup(event, drag_rect)
    
    def handle_mousedragup(self, event, drag_rect):
        pass
    
    def activate(self):
        """The screen is now active and ready to roll"""
        pass
    
    def quit(self, event=None):
        self.engine.quit()
    
    def test_for_keyboard_commands(self):
        # Cmd + Q
        if 113 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[113]:# Cmd has to be pushed first
                self.quit()
    
class FullScreen (Screen):
    fullscreen = True
    
    def __init__(self, engine, preferred_size=None):
        dimensions = self.get_max_size(preferred_size)
        
        super(FullScreen, self).__init__(engine, dimensions = dimensions)
    
    def get_max_size(self, preferred_size=None):
        """Takes the preferred size and gets the closest it can (rounding
        down to a smaller screen). It will always try to get the same ratio,
        if it cannot find the same ratio it will error."""
        
        # Default to max size!
        if preferred_size == None:
            return pygame.display.list_modes()[0]
        
        x, y = preferred_size
        ratio = x/y
        
        found_size = (0,0)
        for sx, sy in pygame.display.list_modes():
            sratio = sx/sy
            
            if sratio != ratio:
                continue
            
            # Make sure it's small enough
            if sx <= x and sy <= y:
                if sx > found_size[0] and sy > found_size[1]:
                    found_size = sx, sy
        
        if found_size != (0,0):
            return found_size
        return None
            
    




