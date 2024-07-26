# Import statements
import pygame as pyg
import sys

from classes.display import Colors
from classes.globals import Globals
from classes.window import WindowManager

from Editor.model_parent import Model
from Editor.ui_overlay import UIOverlay

import modules.typing_handler as t_handler

model = Model()

def Main(winman: WindowManager):
    model.load()
    model.create_model()
    overlay = UIOverlay(winman, model)

    rotating = False
    rotate_up = False
    rotate_down = False
    rotate_left = False
    rotate_right = False
    left_click = False
    adding_line = False

    while True:
        if rotating:
            model.rotate_components([0, 1, 0], (Globals.mouse_position[0] - 1920 / 2) / 2)
        elif rotate_down:
            model.rotate_components([1, 0, 0], -400)
        elif rotate_up:
            model.rotate_components([1, 0, 0], 400)
        elif rotate_left:
            model.rotate_components([0, 1, 0], -400)
        elif rotate_right:
            model.rotate_components([0, 1, 0], 400)

        Globals.mouse_position[0] = pyg.mouse.get_pos()[0] * winman.get_scale()[0]
        Globals.mouse_position[1] = pyg.mouse.get_pos()[1] * winman.get_scale()[1]

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            elif event.type == pyg.KEYDOWN:
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()

                if not overlay.current_popup:
                    if key == pyg.K_DOWN:
                        rotate_down = True
                    elif key == pyg.K_UP:
                        rotate_up = True
                    elif key == pyg.K_LEFT:
                        rotate_left = True
                    elif key == pyg.K_RIGHT:
                        rotate_right = True

                    elif key == pyg.K_r:
                        model.create_model()
                        model.draw_model()

                    elif key == pyg.K_ESCAPE:
                        if adding_line:
                            model.clothes_data["verticies"].pop()
                            adding_line = False
                        model.edit_mode = "none"

                if overlay.current_popup:
                    for field in overlay.current_popup.fields:
                        f = overlay.current_popup.fields[field]
                        if f.active:
                            f.text, Globals.cursor_position = t_handler.handle_text(f.text, key, (shift, caps, ctrl), Globals.cursor_position)

            elif event.type == pyg.KEYUP:
                rotate_down = False
                rotate_up = False
                rotate_left = False
                rotate_right = False

            elif event.type == pyg.MOUSEBUTTONDOWN:                
                if event.button == 1 and model.model_hovered and model.edit_mode != "none":
                    model.add_point()
                    if model.edit_mode == "add_lines":
                        left_click = True
                        adding_line = True
                
                if event.button == 2:
                    rotating = True

                if event.button == 4 or event.button == 5:
                    overlay.scroll(event.button)

            elif event.type == pyg.MOUSEBUTTONUP:
                overlay.mouse_click(event.button)

                if event.button == 1 and model.model_hovered and adding_line:
                    left_click = False
                    model.add_line()
                    adding_line = False
                    
                if event.button == 2:
                    rotating = False

        winman.display.fill(Colors.charcoal)
        model.render(winman.display, not overlay.current_popup)
        overlay.render(winman.display)

        if left_click and len(model.clothes_data["verticies"]):
            pyg.draw.line(winman.display, Colors.red, model.clothes_data["verticies"][-1][:2], model.hovered_point[:2])

        winman.render()
        Globals.clock.tick(Globals.FPS)

if __name__ == "__main__":
    Main()