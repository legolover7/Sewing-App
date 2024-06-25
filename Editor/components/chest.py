import math

from Editor.components.component_base import ModelComponent

class Chest(ModelComponent):
    def __init__(self):
        super().__init__()
        self.control_points = {
            "chest_radius": 0
        }
    
    def generate_model_data(self, components, measurements, top_y):
        super().generate_model_data()

        # Get radii
        uc_radius = measurements["up_chest_depth"] / 2
        lc_radius = measurements["low_chest_depth"] / 2

        # Shoulder calculations to figure out shoulder height
        shoulder_top_x    = self.center_x - (measurements["shoulder_width"] - uc_radius) / 2
        shoulder_bottom_x = self.center_x - (measurements["shoulder_width"] - uc_radius) / 2 
        shoulder_height   = ((shoulder_top_x - shoulder_bottom_x) ** 2 + (self.ctw(measurements["armh_cir"])) ** 2) ** 0.5

        # Get x values
        uc_left_x  = self.center_x - (measurements["up_chest_width"] - uc_radius) / 2
        uc_right_x = self.center_x + (measurements["up_chest_width"] - uc_radius) / 2
        lc_left_x  = self.center_x - (measurements["low_chest_width"] - lc_radius) / 2
        lc_right_x = self.center_x + (measurements["low_chest_width"] - lc_radius) / 2

        # Get y values
        uc_y = top_y + shoulder_height
        lc_y = top_y + measurements["shldr_to_lowchest"]
        
        # Generate sides
        self.generate_tube(uc_left_x, uc_y, uc_radius, lc_left_x, lc_y, lc_radius, -1)
        self.generate_tube(uc_right_x, uc_y, uc_radius, lc_right_x, lc_y, lc_radius, 1)

        # Generate front/back
        self.connect_polygon((uc_left_x, uc_y, uc_radius), (uc_right_x, uc_y, uc_radius), (lc_left_x, lc_y, lc_radius), (lc_right_x, lc_y, lc_radius))
        self.connect_polygon((uc_left_x, uc_y, -uc_radius), (uc_right_x, uc_y, -uc_radius), (lc_left_x, lc_y, -lc_radius), (lc_right_x, lc_y, -lc_radius))

        self.xbounds = [uc_left_x - uc_radius, uc_right_x + uc_radius]
        self.ybounds = [uc_y, lc_y]