import pygame as pyg

from classes.button import *

class Ribbon:
    def __init__(self, size):
        self.x, self.y = (0, 0)
        self.width, self.height = size
        self.size_radios = {
            "small": RadioButton(self, (self.width - 200, 25), "S"),
            "medium": RadioButton(self, (self.width - 150, 25), "M"),
            "large": RadioButton(self, (self.width - 100, 25), "L"),
        }

        self.buttons = {
            "ribbon_hide": CharButton(self, (self.width - 40, 10), (30, 30), Colors.gray2, "<", rotate=270),
            "set_msmts": UnderlineButton(self, (15, 15), "Set Measurements")
        }

    def render(self, surface: pyg.Surface):
        pyg.draw.rect(surface, Colors.gray1, (0, 0, self.width, self.height), border_bottom_left_radius=15, border_bottom_right_radius=15)

        for radio in self.size_radios:
            self.size_radios[radio].render(surface)

        for button in self.buttons:
            self.buttons[button].render(surface)