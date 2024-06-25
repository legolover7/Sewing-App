import pygame as pyg
import json
import time

from classes.button import *
from classes.display import Colors, Fonts
from classes.globals import FilePaths
from classes.input_field import *

from menus.menu_base import MenuBase

class PatternPopup(MenuBase):
    def __init__(self, parent, size: tuple):
        super().__init__(parent, size, popup=True)

        self.buttons = {
            "close_button": CharButton(self, (self.width - 35, 5), (30, 30), char="X"),
            "save": MenuButton(self, (self.width / 2 - 130, self.height - 40), (120, 30), ["Save"]),
            "pattern": MenuButton(self, (self.width / 2 + 10, self.height - 40), (120, 30), ["Pattern"]),
        }

        self.fields = {
            "title": IFBox((50, self.height / 2 - 14, self.width - 100, 28), "Title", Fonts.font_24)
        }

    def render(self, surface: pyg.Surface):
        super().render(surface)

        text_width = Fonts.font_24.size("Save Design/Pattern")[0]
        self.display.blit(Fonts.font_24.render("Save Design/Pattern", True, Colors.aqua), ((self.width - text_width) / 2, 10))

        for name in self.buttons:
            self.buttons[name].render(self.display)

        for field in self.fields:
            f = self.fields[field]
            f.render(self.display)

        surface.blit(self.display, (self.x, self.y))

    def mouse_click(self, button):
        if button == 1:
            if self.buttons["close_button"].collides_mouse:
                self.parent.current_popup = None

            if self.buttons["save"].collides_mouse and self.fields["title"].text != "":
                with open(FilePaths.user_patterns, "r") as file:
                    data = json.load(file)

                with open(FilePaths.user_patterns, "w") as file:
                    data[self.fields["title"].text] = self.parent.model.clothes_data
                    data[self.fields["title"].text]["date_saved"] = time.strftime("%d/%m/%Y - %I:%M%p")
                    file.write(json.dumps(data))

                self.fields["title"].text = ""
                self.parent.current_popup = None

            for field in self.fields:
                self.fields[field].active = False
                if self.fields[field].check_mcollision((Globals.mouse_position[0] - self.x, Globals.mouse_position[1] - self.y)):
                    self.fields[field].active = True
                    Globals.cursor_position = len(self.fields[field].text)