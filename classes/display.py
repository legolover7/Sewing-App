import pygame as pyg
pyg.font.init()

class Colors:
    black = (0, 0, 0)
    charcoal = (25, 25, 25)
    
    gray1 = (50, 50, 50)
    gray2 = (70, 70, 70)
    gray3 = (90, 90, 90)
    gray4 = (120, 120, 120)
    
    white = (255, 255, 255)

    green = (0, 200, 0)
    aqua = (0, 255, 255)
    blue = (0, 0, 200)
    light_blue = (0, 0, 238)
    red = (200, 0, 0)

class Fonts:
    font_18 = pyg.font.SysFont("consolas", 18)
    font_20 = pyg.font.SysFont("consolas", 20)
    font_24 = pyg.font.SysFont("consolas", 24)
    font_26 = pyg.font.SysFont("consolas", 26)
    font_30 = pyg.font.SysFont("consolas", 30)
    font_40 = pyg.font.SysFont("consolas", 40)