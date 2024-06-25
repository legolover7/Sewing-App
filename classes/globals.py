import pygame as pyg

class Globals:
    FPS = 60
    clock = pyg.time.Clock()

    mouse_position = [0, 0]
    cursor_position = 0
    cursor_period = 1.2 * FPS
    cursor_timeout = 5 * cursor_period
    cursor_frame = 0 

class FilePaths:
    user_measurements = "data/user_measurements.json"
    preset_measurements = "data/preset_measurements.json"
    user_patterns = "data/user_patterns.json"