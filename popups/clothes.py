import pygame as pyg
import json

from classes.button import *
from classes.display import Colors, Fonts
from classes.globals import FilePaths
from classes.list_container import *

from menus.menu_base import MenuBase

class ClothesPopup(MenuBase):
    def __init__(self, parent, size: tuple):
        super().__init__(parent, size, popup=True)

        self.selection_buttons = {
            "shirt": MenuButton(self, (self.width / 2 - 337.5, self.height / 2 - 150), (150, 100), ["Shirt"]),
            "pants": MenuButton(self, (self.width / 2 - 162.5, self.height / 2 - 150), (150, 100), ["Pants"]),
            "skirt": MenuButton(self, (self.width / 2 + 12.5,  self.height / 2 - 150), (150, 100), ["Skirt"]),
            "dress": MenuButton(self, (self.width / 2 + 187.5, self.height / 2 - 150), (150, 100), ["Dress"])
        }

        self.buttons = {
            "back": CharButton(self, (10, 10), (30, 30), char="<"),
            "draw": MenuButton(self, (self.width / 2 - 75, self.height - 75), (150, 50), ["Create!"])
        }

        self.radios = {
            "small": RadioButton(self, (self.width / 2 - 200, self.height / 2 + 10), "Small"),
            "medium": RadioButton(self, (self.width / 2 - 200, self.height / 2 + 45), "Medium"),
            "large": RadioButton(self, (self.width / 2 - 200, self.height / 2 + 80), "Large"),
        }
        self.radios["medium"].active = True

        self.container = ListContainer(self, (self.width / 2 , self.height / 2), (337.5, 170))

        # Populate container with saved measurements
        with open(FilePaths.user_measurements, "r") as file:
            data = json.load(file)
            for m in data:
                self.container.contents.append(ListContent(m["title"], m["saved"]))

        self.selected = None
        self.preset_active = True
        self.selection_buttons["shirt"].fg_color = Colors.gray4

    def render(self, surface: pyg.Surface):
        super().render(surface)

        text_width = Fonts.font_30.size("What would you like to make today?")[0]
        self.display.blit(Fonts.font_30.render("What would you like to make today?", True, Colors.aqua), ((self.width - text_width) / 2, 20))

        self.display.blit(Fonts.font_24.render("Presets:", True, Colors.aqua), (self.width / 2 - 210, self.height / 2 - 30))
        self.display.blit(Fonts.font_24.render("Saved Measurements:", True, Colors.aqua), (self.width / 2, self.height / 2 - 30))

        for name in self.selection_buttons:
            self.selection_buttons[name].render(self.display, False)

        for name in self.buttons:
            self.buttons[name].render(self.display)

        for name in self.radios:
            self.radios[name].render(self.display)

        self.container.render(self.display)

        surface.blit(self.display, (self.x, self.y))

    def mouse_click(self, button):
        if button == 1:
            # Clothing option
            active = ""
            for name in self.selection_buttons:
                if self.selection_buttons[name].collides_mouse:
                    active = name
                
            if active != "":
                for name in self.selection_buttons:
                    self.selection_buttons[name].fg_color = Colors.gray2
                    if name == active:
                        self.selection_buttons[name].fg_color = Colors.gray4
                        
            # Preset sizes
            active = ""
            for name in self.radios:
                if self.radios[name].collides_mouse:
                    active = name
                
            if active != "":
                self.preset_active = True
                for name in self.radios:
                    self.radios[name].active = False
                    if name == active:
                        self.radios[name].active = True

                for c in self.container.contents:
                    c.active = False

            # List container
            if collider.collides_point(Globals.mouse_position, (self.x + self.width / 2, self.y + self.height / 2, 337.5, 170)):
                position = self.container.scroll_offset
                active = None
                for c in self.container.contents:
                    # Activate this content and deactivate radio buttons
                    if collider.collides_point(Globals.mouse_position, (self.x + self.width / 2, self.y + self.height / 2 + position, self.container.width - 12, c.height)):
                        active = c
                        for name in self.radios:
                            self.radios[name].active = False
                            self.preset_active = False
                    position += c.height - 2

                if active:
                    for c in self.container.contents:
                        c.active = c == active

            if self.buttons["back"].collides_mouse:
                self.parent.current_popup = self.parent.popups["create"]

            if self.buttons["draw"].collides_mouse:
                self.parent.draw = True

        if button == 6:
            self.parent.current_popup = self.parent.popups["create"]

    def scroll(self, direction):
        if collider.collides_point(Globals.mouse_position, (self.x + self.width / 2, self.y + self.height / 2, 337.5, 170)) and len(self.container.contents) > 3:
            self.container.scroll_offset += direction * 8
            max_scroll = (self.container.contents[0].height - 2) * len(self.container.contents) - 155
            self.container.scroll_offset = min(0, self.container.scroll_offset)
            self.container.scroll_offset = max(-max_scroll, self.container.scroll_offset)