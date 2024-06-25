import pygame as pyg

from classes.button import *
from classes.display import Colors, Fonts
from menus.menu_base import MenuBase

class CreatePopup(MenuBase):
    def __init__(self, parent, size: tuple):
        super().__init__(parent, size, popup=True)

        self.buttons = {
            "clothes": MenuButton(self, (self.width / 2 - 295, self.height / 2 - 50), (180, 100), ["Clothes"]),
            "accessories": MenuButton(self, (self.width / 2 - 90, self.height / 2 - 50), (180, 100), ["Accessories"]),
            "added": MenuButton(self, (self.width / 2 + 115, self.height / 2 - 50), (180, 100), ["Coming soon"]),
            "back": CharButton(self, (10, 10), (30, 30), char="<")
        }

    def render(self, surface: pyg.Surface):
        super().render(surface)

        text_width = Fonts.font_30.size("What would you like to make today?")[0]
        self.display.blit(Fonts.font_30.render("What would you like to make today?", True, Colors.aqua), ((self.width - text_width) / 2, 20))

        for name in self.buttons:
            self.buttons[name].render(self.display)

        surface.blit(self.display, (self.x, self.y))

    def mouse_click(self, button):
        if button == 1:
            if self.buttons["clothes"].collides_mouse:
                self.parent.current_popup = self.parent.popups["clothes"]

            elif self.buttons["back"].collides_mouse:
                self.parent.current_popup = None

        elif button == 6:
            self.parent.current_popup = None