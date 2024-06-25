# Import statements
import pygame as pyg
import json
import sys

from classes.globals import FilePaths, Globals
from classes.window import WindowManager

from menus.welcome import WelcomeMenu

import Editor.control_script as ecs

def Main():
    winman = WindowManager("Sewing App")
    welcome_menu = WelcomeMenu(winman)

    while True:
        for event in pyg.event.get():
            Globals.mouse_position[0] = pyg.mouse.get_pos()[0] * winman.get_scale()[0]
            Globals.mouse_position[1] = pyg.mouse.get_pos()[1] * winman.get_scale()[0]
            
            if event.type == pyg.QUIT:
                winman.quit()

            elif event.type == pyg.KEYDOWN:
                key = event.key
                # mods = pyg.key.get_mods()
                # shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                if key == pyg.K_F1:
                    winman.quit()

                elif key == pyg.K_F11:
                    winman.toggle_fullscreen()
                
                else:
                    welcome_menu.key_press(event.key)

            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    welcome_menu.scroll(event.button)

            elif event.type == pyg.MOUSEBUTTONUP:
                welcome_menu.mouse_click(event.button)

        if welcome_menu.draw:
            # Yuck
            if welcome_menu.popups["clothes"].preset_active:
                for name in welcome_menu.popups["clothes"].radios:
                    if welcome_menu.popups["clothes"].radios[name].active:
                        with open(FilePaths.preset_measurements, "r") as file:
                            data = json.load(file)
                            ecs.model.measurements = data[name[0]]
            else:
                with open(FilePaths.user_measurements, "r") as file:
                    data = json.load(file)
                    for c in welcome_menu.popups["clothes"].container.contents:
                        if c.active:
                            title = c.title
                    
                    for m in data:
                        if m["title"] == title:
                            ecs.model.measurements = m["values"]
                            ecs.model.type = m["sex"]

            ecs.Main(winman)

        winman.display.fill((200, 50, 100))
        welcome_menu.render(winman.display)
        
        winman.render()
        Globals.clock.tick(Globals.FPS)

if __name__ == "__main__":
    Main()