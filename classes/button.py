import pygame as pyg

from classes.display import Colors, Fonts
from classes.globals import Globals

import modules.collider as collider

class ButtonBase:
    def __init__(self, parent, position, size, text, bg_color, fg_color, text_color, font: pyg.font.Font):
        self.parent = parent
        self.x, self.y = position
        self.width, self.height = size
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text_color = text_color
        self.font = font

        self.border_size = 2
        self.border_radius = 10

    @property
    def collides_mouse(self) -> bool:
        return pyg.Rect(self.x + self.parent.x, self.y + self.parent.y, self.width, self.height).collidepoint(Globals.mouse_position)        

class MenuButton(ButtonBase):
    def __init__(self, parent, position, size, textlines):
        super().__init__(parent, position, size, textlines, Colors.gray1, Colors.gray2, Colors.white, Fonts.font_24)

    def render(self, surface: pyg.Surface, scale=True):
        x, y = self.x, self.y
        width, height = self.width, self.height
        if self.collides_mouse and scale:
            width *= 1.1
            height *= 1.1
            x -= (width - self.width) / 2
            y -= (height - self.height) / 2

        pyg.draw.rect(surface, self.bg_color, (x, y, width, height), border_radius=self.border_radius)
        pyg.draw.rect(surface, self.fg_color, (x + self.border_size, y + self.border_size, 
                                               width - self.border_size * 2, height - self.border_size * 2), border_radius=self.border_radius)

        font = self.font
        if self.collides_mouse and scale:
            font = Fonts.font_26

        line_height = font.size("A")[1] + 2
        start_y = y + height / 2 - (len(self.text) / 2 * line_height)
        for i, line in enumerate(self.text):
            text_width, text_height = font.size(line)
            surface.blit(font.render(line, True, self.text_color), (x + (width - text_width) / 2, start_y + line_height * i))

class RadioButton:
    def __init__(self, parent, position, text):
        self.parent = parent
        self.x, self.y = position
        self.text = text
        self.active = False
        self.width = 0

    @property
    def collides_mouse(self) -> bool:
        return collider.collides_point(Globals.mouse_position, (self.x + self.parent.x - 10, self.y + self.parent.y - self.height / 2, self.width + 2, self.height + 4))

    def render(self, surface: pyg.Surface):
        pyg.draw.circle(surface, Colors.gray2, (self.x, self.y), 10)
        pyg.draw.circle(surface, Colors.gray1, (self.x, self.y), 9)

        if self.active:
            pyg.draw.circle(surface, Colors.gray4, (self.x, self.y), 7)

        self.width, self.height = Fonts.font_24.size(self.text)
        self.width += 28
        surface.blit(Fonts.font_24.render(self.text, True, Colors.white), (self.x + 16, self.y - self.height / 2 + 1))

class CharButton(ButtonBase):
    def __init__(self, parent, position, size, highlight_color=Colors.gray1, char="<", rotate=0):
        super().__init__(parent, position, size, char, Colors.charcoal, highlight_color, Colors.white, Fonts.font_24)
        self.rotate = rotate

    def render(self, surface: pyg.Surface):
        if self.collides_mouse:
            pyg.draw.rect(surface, self.fg_color, (self.x, self.y, self.width, self.height), border_radius=4)

        text_width, text_height = self.font.size(self.text)
        char = pyg.transform.rotate(self.font.render(self.text, True, self.text_color), self.rotate)
        if self.rotate == 90 or self.rotate == 270:
            text_width, text_height = text_height, text_width
        surface.blit(char, (self.x + (self.width - text_width) / 2 - (6 if self.rotate == 90 or self.rotate == 270 else 0), self.y + (self.height - text_height) / 2))

class UnderlineButton(ButtonBase):
    def __init__(self, parent, position, text):
        super().__init__(parent, position, (0, 0), text, Colors.charcoal, Colors.white, Colors.white, Fonts.font_20)

    @property
    def collides_mouse(self) -> bool:
        text_width, text_height = self.font.size(self.text)
        return collider.collides_point(Globals.mouse_position, (self.x, self.y, text_width, text_height + 2))

    def render(self, surface: pyg.Surface):
        text_width, text_height = self.font.size(self.text)
        surface.blit(self.font.render(self.text, True, self.text_color), (self.x, self.y))

        if self.collides_mouse:
            pyg.draw.line(surface, self.fg_color, (self.x, self.y + text_height), (self.x + text_width, self.y + text_height))