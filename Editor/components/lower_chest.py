import math

from Editor.components.component_base import ModelComponent

class LowerChest(ModelComponent):
    def __init__(self):
        super().__init__()
    
    def generate_model_data(self, components, measurements, top_y):
        super().generate_model_data()

        # Get radii
        lc_radius    = measurements["low_chest_depth"] / 2
        waist_radius = measurements["waist_width"] / 4

        # Get x values
        lc_left_x     = self.center_x - (measurements["low_chest_width"] - lc_radius) / 2
        lc_right_x    = self.center_x + (measurements["low_chest_width"] - lc_radius) / 2
        waist_left_x  = self.center_x - (measurements["waist_width"] - waist_radius) / 2
        waist_right_x = self.center_x + (measurements["waist_width"] - waist_radius) / 2

        self.x_dist = -abs(waist_left_x - waist_radius - (lc_left_x - lc_radius))

        # Get y values
        lc_y    = top_y + measurements["shldr_to_lowchest"]
        waist_y = top_y + measurements["fbod_len"]
        
        # Generate sides
        self.generate_tube(lc_left_x, lc_y, lc_radius, waist_left_x, waist_y, waist_radius, -1)
        self.generate_tube(lc_right_x, lc_y, lc_radius, waist_right_x, waist_y, waist_radius, 1)

        # Generate front/back
        self.connect_polygon((lc_left_x, lc_y, lc_radius), (lc_right_x, lc_y, lc_radius), (waist_left_x, waist_y, waist_radius), (waist_right_x, waist_y, waist_radius))
        self.connect_polygon((lc_left_x, lc_y, -lc_radius), (lc_right_x, lc_y, -lc_radius), (waist_left_x, waist_y, -waist_radius), (waist_right_x, waist_y, -waist_radius))

        self.xbounds = [lc_left_x - lc_radius, lc_right_x + lc_radius]
        self.ybounds = [lc_y, waist_y]