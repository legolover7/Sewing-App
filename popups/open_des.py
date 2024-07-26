import pygame as pyg
import json

from classes.button import *
from classes.display import Colors, Fonts
from classes.globals import FilePaths
from classes.input_field import *
from classes.list_container import *

from menus.menu_base import MenuBase

class OpenDesPopup(MenuBase):
    def __init__(self, parent, size: tuple):
        super().__init__(parent, size, popup=True)

        self.buttons = {
            "close": CharButton(self, (self.width - 35, 5), (30, 30), char="X"),
            "load": MenuButton(self, (self.width / 2 - 110, self.height - 50), (100, 30), ["Load"]),
            "delete": MenuButton(self, (self.width / 2 + 10, self.height - 50), (100, 30), ["Delete"]),
        }

        self.fields = {
        }

        self.container = ListContainer(self, (self.width / 2 - 150, 50), (300, self.height - 120))

    def refresh(self):
        self.container.contents = []
        with open(FilePaths.user_patterns, "r") as file:
            self.data = json.load(file)

            for pattern in self.data:
                self.container.contents.append(ListContent(pattern, self.data[pattern]["date_saved"]))

    def render(self, surface: pyg.Surface):
        super().render(surface)

        text_width = Fonts.font_24.size("Load design")[0]
        self.display.blit(Fonts.font_24.render("Load design", True, Colors.aqua), ((self.width - text_width) / 2, 10))

        for name in self.buttons:
            self.buttons[name].render(self.display)

        for field in self.fields:
            f = self.fields[field]
            f.render(self.display)

        self.container.render(self.display)

        surface.blit(self.display, (self.x, self.y))

    def mouse_click(self, button):
        if button == 1:
            if self.buttons["close"].collides_mouse:
                self.parent.current_popup = None

            if self.buttons["load"].collides_mouse and self.selection:
                self.parent.model.create_model()
                self.parent.model.draw_model()
                self.parent.model.clothes_data = self.data[self.selection.title]
                self.parent.current_popup = None

            if self.buttons["delete"].collides_mouse and self.selection:
                self.container.contents.remove(self.selection)
                del self.data[self.selection.title]
                
                with open(FilePaths.user_patterns, "w") as file:
                    file.write(json.dumps(self.data))

            # List container
            if collider.collides_point(Globals.mouse_position, (self.x + self.container.x, self.y + self.container.y, self.container.width, self.height - 60)):
                position = self.container.scroll_offset
                self.selection = None
                for c in self.container.contents:
                    if collider.collides_point(Globals.mouse_position, (self.x + self.width / 2 - 150, self.y + 50 + position, self.container.width - 12, c.height)):
                        self.selection = c
                    position += c.height - 2

                if self.selection:
                    for c in self.container.contents:
                        c.active = c == self.selection

            for field in self.fields:
                self.fields[field].active = False
                if self.fields[field].check_mcollision((Globals.mouse_position[0] - self.x, Globals.mouse_position[1] - self.y)):
                    self.fields[field].active = True
                    Globals.cursor_position = len(self.fields[field].text)

    def scroll(self, direction):
        if collider.collides_point(Globals.mouse_position, (self.x + self.container.x, self.y + self.container.y, self.container.width, self.height - 60)) and len(self.container.contents) > 3:
            self.container.scroll_offset += direction * 8
            max_scroll = (self.container.contents[0].height - 2) * len(self.container.contents) - 155
            self.container.scroll_offset = min(0, self.container.scroll_offset)
            self.container.scroll_offset = max(-max_scroll, self.container.scroll_offset)