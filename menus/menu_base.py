import pygame as pyg

from classes.display import Colors
from classes.globals import Globals

import modules.collider as collider

class MenuBase:
    """A base class for menu and popup components"""
    
    def __init__(self, parent, size: tuple, centered=True, popup=False):
        self.parent = parent
        self.width, self.height = size
        self.display = pyg.Surface(size)
        self.x, self.y = (0, 0)
        self.centered = centered
        self.ispopup = popup
        
        self.display.set_colorkey((0, 0, 0))

    def render(self, surface: pyg.Surface):
        """Renders this component to the screen"""
        if self.centered:
            x = (surface.get_width() - self.display.get_width()) / 2
            y = (surface.get_height() - self.display.get_height()) / 2
        else:
            x, y = (0, 0)

        self.x, self.y = x, y

        if self.ispopup:
            pyg.draw.rect(self.display, Colors.gray1, (0, 0, self.display.get_width(), self.display.get_height()), border_radius=10)
            pyg.draw.rect(self.display, Colors.charcoal, (2, 2, self.display.get_width() - 4, self.display.get_height() - 4), border_radius=10)

    def mouse_click(self, button):
        pass
    
    def collides_mouse(self):
        return collider.collides_point(Globals.mouse_position, (self.x, self.y, self.display.get_width(), self.display.get_height()))