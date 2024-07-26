import pygame as pyg

from classes.button import *
from classes.display import Colors, Fonts
from classes.globals import Globals
from classes.window import WindowManager

from menus.menu_base import MenuBase

class SettingsMenu(MenuBase):
    def __init__(self, winman: WindowManager):
        super().__init__(None, winman.get_size(), False)
        self.winman = winman
        self.toggle_settings = False

        self.buttons = {
            "back": MenuButton(self, (20, 20), (100, 40), ["Back"])
        }

    def render(self, surface: pyg.Surface):
        self.display.fill(Colors.charcoal)

        for button in self.buttons:
            self.buttons[button].render(self.display)

        surface.blit(self.display, (0, 0))

    def mouse_click(self, button):
        if button == 1:
            if self.buttons["back"].collides_mouse:
                self.toggle_settings = True