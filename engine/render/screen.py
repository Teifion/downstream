from __future__ import division

import time

import pygame
from pygame.locals import *

from engine.libs import screen_lib

class Screen (object):
    facings = 360/4# The number of different angles we'll draw
    
    def __init__(self, engine, dimensions, fullscreen=False):
        super(Screen, self).__init__()
        
        self.fullscreen = fullscreen
        
        if dimensions == None:
            self.fullscreen = True
        
        self.actors = {}
        self.controls = {}
        
        self.name = ""
        self.engine = engine
        self.size = dimensions
        
        # FPS
        self._next_redraw = time.time()
        self._redraw_delay = screen_lib.set_fps(self, 30)
        
        self.image_cache = {}
        
        self.mouse_is_down = False
        self.keys_down = {}
        self.scroll_x, self.scroll_y = 0, 0
        self.mouse = [0,0]
        self.mouse_down_at = [0,0]
        
        self.background_image = None
        self.background = (200, 200, 200)# Default to a grey background
        
        self.surf = pygame.Surface(dimensions)
        
        if self.fullscreen:
            self.switch_to_fullscreen()
        
        self._last_mouseup = [None, -1]
        self._double_click_interval = 0.25
        
        self.transition = None
        self.transition_frame = -1
        self.on_transition = None
        self.on_transition_args = None
        self.on_transition_kwargs = None
    
    def begin_transition(self, mode, callback, args=[], kwargs={}, trans_args=[], trans_kwargs={}):
        self.on_transition = callback
        self.on_transition_args = []
        self.on_transition_kwargs = {}
        
        self.transition = screen_lib.transitions[mode](self, *trans_args, **trans_kwargs)
    
    def activate(self):
        """Called when activated after a screen change"""
        if self.fullscreen:
            self.switch_to_fullscreen()
        else:
            self.switch_to_windowed()
    
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
        if time.time() < self._next_redraw:
            return
        
        surf = self.engine.display
        
        if type(self.background) == tuple or type(self.background) == list:
            surf.fill(self.background)
        else:
            self.background = self.background_image.copy()
            surf.blit(self.background, pygame.Rect(0, 0, self.size[0], self.size[1]))
        
        self.draw_actors()
        self.draw_controls()
        self.draw_transition()
        self.post_redraw()
        
        pygame.display.flip()
        
        self._next_redraw = time.time() + self._redraw_delay
    
    def post_redraw(self):
        """Allows us to append functionality to the redraw function"""
        pass
    
    def draw_actors(self):
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
    
    def draw_controls(self):
        surf = self.engine.display
        
        # We use all of this to draw the controls in order
        # of priority (high priority goes at the top of the screen)
        priorities = set()
        control_sets = {}
        for i, c in self.controls.items():
            p = c.draw_priority
            if p not in control_sets: control_sets[p] = []
            
            control_sets[p].append(i)
            priorities.add(c.draw_priority)
        
        priorities = list(priorities)
        priorities.sort()
        priorities.reverse()
        
        # Panels, unlike actors we draw all of them unless they
        # tell us not to
        for p in priorities:
            for i in control_sets[p]:
                c = self.controls[i]
                if c.visible:
                    c.update()
                    if c.blit_image:
                        surf.blit(*c.image())
                    else:
                        c.draw(surf)
    
    def draw_transition(self):
        surf = self.engine.display
        
        # Potentially a transition too
        if self.transition != None:
            self.transition_frame += 1
            r = self.transition(self.transition_frame)
            
            if r == None:
                self.on_transition(*self.on_transition_args, **self.on_transition_kwargs)
                return
    
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
        
        for i, c in self.controls.items():
            if c.button_down != None:
                if c.contains(event.pos):
                    try:
                        c.button_down(*c.button_down_args, **c.button_down_kwargs)
                    except Exception as e:
                        print("Func: %s" % c.button_down)
                        print("Args: %s" % c.button_down_args)
                        print("Kwargs: %s" % c.button_down_kwargs)
                        raise
        
        self.mouse_is_down = True
        self.handle_mousedown(event)
    
    def handle_mousedown(self, event):
        pass
    
    def _handle_mouseup(self, event):
        if time.time() <= self._last_mouseup[1] + self._double_click_interval:
            return self._handle_doubleclick(self._last_mouseup[0], event)
        
        self._last_mouseup = [event, time.time()]
        real_mouse_pos = (event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y)
        
        for i, c in self.controls.items():
            if c.button_up != None:
                if c.contains(event.pos):
                    try:
                        c.button_up(*c.button_up_args, **c.button_up_kwargs)
                    except Exception as e:
                        print("Func: %s" % c.button_up)
                        print("Args: %s" % c.button_up_args)
                        print("Kwargs: %s" % c.button_up_kwargs)
                        raise
            elif c.accepts_mouseup:
                if c.contains(event.pos):
                    c.handle_mouseup(event)
                    
            
        
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
    
    def quit(self, event=None):
        self.engine.quit()
    
    def test_for_keyboard_commands(self):
        # Cmd + Q
        if 113 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[113]:# Cmd has to be pushed first
                self.quit()
    
    def get_max_window_size(self, preferred_size=None):
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
    
    def switch_to_fullscreen(self):
        self.fullscreen = True
        
        dimensions = self.get_max_window_size(self.size)
        
        # TODO work out if it's okay to use the HWSURFACE flag
        # or if I need to stick wih FULLSCREEN
        self.engine.display = pygame.display.set_mode(dimensions, FULLSCREEN)
    
    def switch_to_windowed(self):
        self.fullscreen = False
        
        self.engine.display = pygame.display.set_mode(self.size)

