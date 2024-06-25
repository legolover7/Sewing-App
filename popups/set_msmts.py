import pygame as pyg

from classes.button import *
from classes.display import Colors, Fonts
from classes.input_field import *

from menus.menu_base import MenuBase

class MSMTPopup(MenuBase):
    def __init__(self, parent, size: tuple):
        super().__init__(parent, size, popup=True)

        self.buttons = {
            "close_button": CharButton(self, (self.width - 35, 5), (30, 30), char="X")
        }

        self.fields = {
            "Height": IFBox((10, 30, 80, 28), str(self.parent.model.raw_data["height"]), Fonts.font_20, 6),
            "Bust Cir": IFBox((120, 30, 80, 28), str(self.parent.model.raw_data["mid_chest_cir"]), Fonts.font_20, 6),
            "Waist Cir": IFBox((10, 90, 80, 28), str(self.parent.model.raw_data["waist_cir"]), Fonts.font_20, 6),
            "Hip Cir": IFBox((120, 90, 80, 28), str(self.parent.model.raw_data["hip_cir"]), Fonts.font_20, 6),
            "Knee Cir": IFBox((10, 150, 80, 28), str(self.parent.model.raw_data["knee_cir"]), Fonts.font_20, 6),
            "Ankle Cir": IFBox((120, 150, 80, 28), str(self.parent.model.raw_data["ankle_cir"]), Fonts.font_20, 6),
        }

    def render(self, surface: pyg.Surface):
        super().render(surface)

        self.x = self.parent.width / 2 + self.parent.width / 6

        for name in self.buttons:
            self.buttons[name].render(self.display)

        for field in self.fields:
            f = self.fields[field]
            self.display.blit(Fonts.font_20.render(field, True, Colors.white), (f.x, f.y - 20))
            f.render(self.display)

        surface.blit(self.display, (self.x, self.y))

    def mouse_click(self, button):
        if button == 1:
            if self.buttons["close_button"].collides_mouse:
                self.parent.current_popup = None

            for field in self.fields:
                self.fields[field].active = False
                if self.fields[field].check_mcollision((Globals.mouse_position[0] - self.x, Globals.mouse_position[1] - self.y)):
                    self.fields[field].active = True
                    Globals.cursor_position = len(self.fields[field].text)