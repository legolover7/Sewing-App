import pygame as pyg

from classes.display import Colors, Fonts
from classes.globals import Globals

import modules.collider as collider

class ListContainer:
    def __init__(self, parent, position: tuple, size: tuple):
        self.parent = parent
        self.x, self.y = position
        self.width, self.height = size
        self.display = pyg.Surface((self.width - 12, self.height - 12))
        self.display.set_colorkey(Colors.black)
        self.scroll_offset = 0

        self.contents: list[ListContent] = []

    def render(self, surface: pyg.Surface):
        self.display.fill(Colors.charcoal)
        pyg.draw.rect(surface, Colors.gray2, (self.x, self.y, self.width, self.height), border_radius=15)
        pyg.draw.rect(surface, Colors.charcoal, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=15)

        self.display.fill(Colors.black)
        position = self.scroll_offset
        for c in self.contents:
            c.render(self.display, self, position, self.width - 12)
            position += c.height - 2

        surface.blit(self.display, (self.x + 6, self.y + 6))

class ListContent:
    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
        self.active = False

        self.height = Fonts.font_24.size(self.title)[1] + Fonts.font_20.size(self.subtitle)[1] + 10

    def render(self, surface: pyg.Surface, parent, position: int, width: int):
        pyg.draw.rect(surface, Colors.gray2, (0, position, width, self.height), border_radius=15)

        color = Colors.gray2 if self.active or collider.collides_point(Globals.mouse_position, (parent.parent.x + parent.x, parent.parent.y + parent.y + position, width, self.height)) else Colors.gray1
        pyg.draw.rect(surface, color, (2, position + 2, width - 4, self.height - 4), border_radius=15)

        text_height = Fonts.font_24.size(self.title)[1]
        surface.blit(Fonts.font_24.render(self.title, True, Colors.white), (6, position + 4))

        surface.blit(Fonts.font_20.render(self.subtitle, True, Colors.gray4), (6, position + text_height + 6))
        