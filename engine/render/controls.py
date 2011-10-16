import pygame
from pygame.locals import *

def draw_text(surface, text, position, colour=(0,0,0),
    font="Helvetica", size=20, antialias=1, bold=False, italic=False,
    font_obj=None):
    
    if not font_obj:
        font_obj = pygame.font.SysFont(font, size)
        
        font_obj.set_bold(bold)
        font_obj.set_italic(italic)
    
    if type(position) == str:
        position = 10, 10
    
    textobj = font_obj.render(text, antialias, colour)
    textrect = textobj.get_rect()
    textrect.topleft = position
    surface.blit(textobj, textrect)

class Control (object):
    # When set to True the screen will assume that .draw()
    # returns an image for it to blit, if not then it will
    # pass a copy of the surface to the control for
    # it to draw itself as need be
    blit_image = False
    
    def __init__(self, position, size):
        super(Control, self).__init__()
        
        self.rect = pygame.Rect(0,0,0,0)
        self.rect.topleft = position
        self.rect.size = size
        
        self.visible = True
        
        self.button_down = None
        self.button_up = None
        
        self.button_up_args = []
        self.button_down_args = []
        
        self.button_up_kwargs = {}
        self.button_down_kwargs = {}
        
        
        self.update()
    
    def contains(self, position):
        if self.rect.left <= position[0] <= self.rect.right:
            if self.rect.top <= position[1] <= self.rect.bottom:
                return True
        
        return False
    
    def update(self):
        pass
    
    # Some control types will need to be told when to redraw themselves
    def redraw(self, *args, **kwargs):
        raise Exception("redraw() is not accepted by this control type")
    
    def draw(self, surf, offset=(0,0)):
        if self.blit_image:
            raise Exception("This control has blit_image set to True yet the draw() function is being called")
        

class TextDisplay (Control):
    def __init__(self, position, text, font_name="Helvetica", font_size=20, colour=(255,0,0)):
        super(TextDisplay, self).__init__(position, size=(0,0))
        
        self.font = pygame.font.SysFont(font_name, font_size)
        
        self.colour = colour
        self.text = text
        self._last_text = ""
        
        self.bold = False
        self.italic = False
        
        if list(colour) == [255,255,255]:
            self.fill_colour = (0,0,0,0)
        else:
            self.fill_colour = (255,255,255,255)
    
    def update(self):
        if self._last_text != self.text:
            self._last_text = self.text
            
            if self.text == "":
                self.rect = pygame.Rect(-100, -100, 0, 0)
                return
            
            self.image = pygame.Surface(self.font.size(self.text), SRCALPHA)
            self.image.fill(self.fill_colour)
            self.image.set_colorkey(self.fill_colour)
            
            area = Rect(33,33,33,33)
            self.image.fill((255,255,255,255), area, BLEND_RGBA_SUB)
            
            # self.image = pygame.Surface(self.font.size(self.text))
            self.rect = self.image.get_rect()
            self.rect.topleft = self.position
            
            textobj = self.font.render(self.text, 1, self.colour)
            textrect = textobj.get_rect()
            textrect.topleft = (0, 0)
            # self.image.blit(textobj, textrect)
    
    def draw(self, surf, offset=(0,0)):
        pass

class Button (Control):
    def __init__(self, position, size, text, fill_colour=(0,0,0), text_colour=(255, 255, 255)):
        super(Button, self).__init__(position, size)
        
        self.has_updated = False
                
        self.text = text
        self.fill_colour = fill_colour
        self.text_colour = text_colour
    
    def update(self):
        pass
    
    def draw(self, surf, offset=(0,0)):
        surf.fill(self.fill_colour, self.rect)
        
        draw_text(surf, text=self.text, position=(self.rect.left + 10, self.rect.top + 10),
            colour=self.text_colour, font="Helvetica",
            size=20, antialias=1,
            bold=False, italic=False, font_obj=None)

class ImageButton (Button):
    def __init__(self, position, image):
        raise Exception("Not implemented correctly yet")
        
        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        super(ImageButton, self).__init__(position, self.rect.size)
        
        self.has_updated = False
        self.button_down = None
        self.button_up = None
        
        self.button_up_args = []
        self.button_down_args = []
        
        self.button_up_kwargs = {}
        self.button_down_kwargs = {}

class InvisibleButton (Control):
    """Used when we don't want to draw a button
    e.g. it's part of the background or something"""
    def __init__(self, position, size):
        super(InvisibleButton, self).__init__()
        
        self.left, self.top = position
        self.right = self.left + size[0]
        self.bottom = self.top + size[1]
        
        self.button_down = None
        self.button_up = None
        
        self.button_up_args = []
        self.button_down_args = []
        
        self.button_up_kwargs = {}
        self.button_down_kwargs = {}
    
    def contains(self, pos):
        if self.left <= pos[0] <= self.right:
            if self.top <= pos[1] <= self.bottom:
                return True
        
        return False
    
    def draw(self, surf, offset=(0,0)):
        pass

# A panel is used mostly for display but often has much more complicated
# behaviour than the rest of the controls (menus etc)
class Panel (Control):
    always_redraw = False
    accepts_keydown = False
    blit_image = True
    
    def __init__(self, position, size):
        super(Panel, self).__init__(position, size)
        
        # When set to true the menu will scroll with the screen
        # much like an actor will
        self.scrolls = False
        
        # Used for caching images as panels don't change that often
        self.changed = False
        self.always_changed = False
        self._image = None
    
    def contains(self, point):
        if self.position.left <= point[0] <= self.position.right:
            if self.position.top <= point[1] <= self.position.bottom:
                return True
    
    def image(self):
        # Try to use the cached version
        if self._image != None and not self.changed and not self.always_redraw and not self.always_changed:
            return self._image, self.rect
        
        # Draw the iamge
        self.draw()
        
        return self._image, self.rect
    
    def draw(self, *args, **kwargs):
        raise Exception("{0}.draw() is not implemented".format(self.__class__))
    
    def handle_mousedrag(self, event):
        pass
    
    def handle_mouseup(self, event, drag=False):
        raise Exception("{0}.handle_mouseup() is not implemented".format(self.__class__))

    def handle_doubleclick(self, first_click, second_click):
        return self.handle_mouseup(second_click)