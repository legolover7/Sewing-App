# Import statements
import pygame as pyg
import sys

from classes.display import Colors
from classes.globals import Globals
from classes.window import WindowManager

from Editor.model.model import Model
from Editor.ui_overlay import UIOverlay

import modules.typing_handler as t_handler

model = Model()

def Main(winman: WindowManager):
    model.setup()
    model.create_model()
    overlay = UIOverlay(winman, model)

    left_click = False
    adding_line = False

    rotation_keys = {
        pyg.K_a: False,
        pyg.K_LEFT: False,
        pyg.K_d: False,
        pyg.K_RIGHT: False
    }

    rotate_vert = False

    while True:
        if rotation_keys[pyg.K_a] or rotation_keys[pyg.K_LEFT]:
            model.rotate_model([0, 1, 0], -1)
        elif rotation_keys[pyg.K_d] or rotation_keys[pyg.K_RIGHT]:
            model.rotate_model([0, 1, 0], 1)

        if pyg.key.get_pressed()[pyg.K_UP] and rotate_vert:
            model.rotate_model([1, 0, 0], 1)
        if pyg.key.get_pressed()[pyg.K_DOWN] and rotate_vert:
            model.rotate_model([1, 0, 0], -1)

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
                    if key == pyg.K_r:
                        model.create_model()

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

            elif event.type == pyg.MOUSEBUTTONDOWN:                
                if event.button == 1 and model.model_hovered and model.edit_mode != "none":
                    model.add_point()
                    if model.edit_mode == "add_lines":
                        left_click = True
                        adding_line = True

                if event.button == 4 or event.button == 5:
                    overlay.scroll(event.button)

            elif event.type == pyg.MOUSEBUTTONUP:
                overlay.mouse_click(event.button)

                if event.button == 1 and model.model_hovered and adding_line:
                    left_click = False
                    model.add_line()
                    adding_line = False

        # Render
        winman.display.fill(Colors.charcoal)
        model.render(winman.display)
        overlay.render(winman.display)

        # Rotation update
        for key in rotation_keys:
            rotation_keys[key] = pyg.key.get_pressed()[key]

        if left_click and len(model.clothes_data["verticies"]):
            pyg.draw.line(winman.display, Colors.red, model.clothes_data["verticies"][-1][:2], model.hovered_point[:2])

        winman.render()
        Globals.clock.tick(Globals.FPS)

if __name__ == "__main__":
    Main()