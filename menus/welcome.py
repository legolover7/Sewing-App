import pygame as pyg

from classes.display import Colors, Fonts
from classes.window import WindowManager
from classes.button import MenuButton

import modules.collider as collider

from menus.menu_base import MenuBase
from menus.settings import SettingsMenu
from popups.create import CreatePopup
from popups.clothes import ClothesPopup

class WelcomeMenu(MenuBase):
    def __init__(self, winman: WindowManager):
        super().__init__(None, winman.get_size(), False)
        self.winman = winman
        self.draw = False
        self.toggle_settings = False

        self.buttons = {
            "create_pattern": MenuButton(self, (winman.width / 2 - 175, winman.height / 2 - 50), (150, 100), ["+", "Create new", "pattern"]),
            "edit_pattern": MenuButton(self, (winman.width / 2 + 25, winman.height / 2 - 50), (150, 100), ["~", "Edit a", "pattern"]),
            "settings": MenuButton(self, (winman.width / 2 - 65, winman.height / 2 + 335), (130, 50), ["Settings"]),
            "quit": MenuButton(self, (winman.width / 2 - 50, winman.height / 2 + 400), (100, 50), ["Quit"]),
        }
        
        self.current_popup = None
        self.popups = {
            "create": CreatePopup(self, (winman.width / 2, winman.height / 2)),
            "clothes": ClothesPopup(self, (winman.width / 2, winman.height / 2))
        }

    def render(self, surface: pyg.Surface):
        self.display.fill(Colors.charcoal)

        text_width = Fonts.font_40.size("Sewing App")[0]
        self.display.blit(Fonts.font_40.render("Sewing App", True, Colors.aqua), ((self.display.get_width() - text_width) / 2, 150))

        for name in self.buttons:
            self.buttons[name].render(self.display, self.current_popup==None)

        if self.current_popup:
            self.display.blit(self.winman.dimmed_display, (0, 0))
            super().render(surface)
            self.current_popup.render(self.display)

        else:
            super().render(surface)

        surface.blit(self.display, (0, 0))

    def mouse_click(self, button):
        if self.current_popup == None:
            if button == 1:
                if self.buttons["create_pattern"].collides_mouse:
                    self.current_popup = self.popups["create"]
                
                if self.buttons["quit"].collides_mouse:
                    self.winman.quit()

                if self.buttons["settings"].collides_mouse:
                    self.toggle_settings = True

        else:
            if not self.current_popup.collides_mouse() and button == 1:
                self.current_popup = None
            else:
                self.current_popup.mouse_click(button)

    def scroll(self, button):
        if self.current_popup == self.popups["clothes"]:
            self.popups["clothes"].scroll(-1 if button == 5 else 1)

    def key_press(self, key):
        if key == pyg.K_ESCAPE and self.current_popup:
            self.current_popup = None