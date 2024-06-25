import pygame as pyg

from classes.button import *
from classes.display import Colors, Fonts
from classes.window import WindowManager

from Editor.ribbon import Ribbon
from Editor.model_parent import Model
from popups.set_msmts import MSMTPopup
from popups.pattern import PatternPopup
from popups.open_des import OpenDesPopup

class UIOverlay:
    def __init__(self, winman: WindowManager, model: Model):
        self.x, self.y = (0, 0)
        self.winman = winman
        self.model = model
        self.width, self.height = winman.get_size()

        self.display = pyg.Surface(winman.get_size())
        self.display.set_colorkey((1, 1, 1))
        self.show_ribbon = True

        self.ribbon = Ribbon((self.display.get_width(), 50))
        self.ribbon_show = CharButton(self, (self.width - 40, 0), (30, 30), Colors.gray2, ">", rotate=270)

        self.buttons = {
            "add_points": MenuButton(self, (15, 100), (160, 60), ["Add Points"]),
            "add_lines": MenuButton(self, (15, 175), (160, 60), ["Add Lines"]),
            "load_design": MenuButton(self, (15, 250), (160, 60), ["Open Design"]),
            "pattern": MenuButton(self, (self.width / 2 - 100, self.height - 50), (200, 40), ["Pattern"])
        }

        self.popups = {
            "msmts": MSMTPopup(self, (self.width / 4, self.height / 2)),
            "pattern": PatternPopup(self, (self.width / 4, self.height / 4)),
            "load_design": OpenDesPopup(self, (self.width / 4, self.height / 3))
        }
        self.popups["msmts"].x = self.display.get_width() / 2 + 100
        self.current_popup = None

    def render(self, surface: pyg.Surface):
        self.display.fill((1, 1, 1))

        if self.show_ribbon:
            self.ribbon.render(self.display)
        else:
            self.ribbon_show.render(self.display)

        for button in self.buttons:
            if button == self.model.edit_mode:
                self.buttons[button].fg_color = Colors.gray4
            else:
                self.buttons[button].fg_color = Colors.gray2
            self.buttons[button].render(self.display)

        # Rotate icon
        # pyg.draw.line(self.display, Colors.gray3, (10, self.height - 35), (60, self.height - 35))
        # pyg.draw.line(self.display, Colors.gray3, (10, self.height - 35), (18, self.height - 43))
        # pyg.draw.line(self.display, Colors.gray3, (10, self.height - 35), (18, self.height - 27))
        # pyg.draw.line(self.display, Colors.gray3, (60, self.height - 35), (52, self.height - 43))
        # pyg.draw.line(self.display, Colors.gray3, (60, self.height - 35), (52, self.height - 27))

        # pyg.draw.line(self.display, Colors.gray3, (35, self.height - 10), (35, self.height - 60))
        # pyg.draw.line(self.display, Colors.gray3, (35, self.height - 10), (27, self.height - 18))
        # pyg.draw.line(self.display, Colors.gray3, (35, self.height - 10), (43, self.height - 18))
        # pyg.draw.line(self.display, Colors.gray3, (35, self.height - 60), (27, self.height - 52))
        # pyg.draw.line(self.display, Colors.gray3, (35, self.height - 60), (43, self.height - 52))

        if self.current_popup:
            self.current_popup.render(self.display)

        surface.blit(self.display, (0, 0))

    def mouse_click(self, button):
        if button == 1:
            active = ""
            for name in self.ribbon.size_radios:
                if self.ribbon.size_radios[name].collides_mouse:
                    active = name
                
            if active != "":
                for name in self.ribbon.size_radios:
                    self.ribbon.size_radios[name].active = False
                    if name == active:
                        self.ribbon.size_radios[name].active = True


            # Ribbon interactions
            if self.show_ribbon:
                if self.ribbon.buttons["ribbon_hide"].collides_mouse:
                    self.show_ribbon = False
                elif self.ribbon.buttons["set_msmts"].collides_mouse:
                    self.current_popup = self.popups["msmts"]
                    
            elif not self.show_ribbon and self.ribbon_show.collides_mouse:
                self.show_ribbon = True

            # Button interactions
            if self.buttons["add_points"].collides_mouse and not self.current_popup:
                self.model.edit_mode = "add_points"
            if self.buttons["add_lines"].collides_mouse and not self.current_popup:
                self.model.edit_mode = "add_lines"
            if self.buttons["load_design"].collides_mouse:
                self.current_popup = self.popups["load_design"]
                self.current_popup.refresh()

            if self.buttons["pattern"].collides_mouse and len(self.model.clothes_data["points"]):
                self.current_popup = self.popups["pattern"]

            if self.current_popup:
                self.model.edit_mode = "none"
                self.current_popup.mouse_click(button)

    def scroll(self, button):
        if self.current_popup == self.popups["load_design"]:
            self.popups["load_design"].scroll(-1 if button == 5 else 1)