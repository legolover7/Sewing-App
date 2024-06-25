import pygame as pyg

from classes.display import Colors

from Editor.components.component_base import ModelComponent

class Abdomen(ModelComponent):
    def __init__(self):
        super().__init__()
    
    def generate_model_data(self, components, measurements, top_y):
        super().generate_model_data()

        # Get radii
        # HIP RADIUS NEEDS TO BE CHANGED, NEED WAIST DEPTH / 2
        waist_radius = measurements["waist_width"] / 4
        hip_radius = measurements["hip_width"] / 4

        # Get x values
        waist_left_x  = self.center_x - (measurements["waist_width"] - waist_radius) / 2
        waist_right_x = self.center_x + (measurements["waist_width"] - waist_radius) / 2
        hip_left_x    = self.center_x - (measurements["hip_width"] / 2 - hip_radius)
        hip_right_x   = self.center_x + (measurements["hip_width"] / 2 - hip_radius)

        self.x_dist = abs(hip_left_x - hip_radius - (waist_left_x - waist_radius))
        self.add_x = True

        # Get y values
        waist_y = top_y + measurements["fbod_len"]
        hip_y   = waist_y + measurements["waist_to_hip_len"]

        # Generate sides
        self.generate_tube(waist_left_x, waist_y, waist_radius, hip_left_x, hip_y, hip_radius, -1)
        self.generate_tube(waist_right_x, waist_y, waist_radius, hip_right_x, hip_y, hip_radius, 1)

        # Generate front/back
        self.connect_polygon((waist_left_x, waist_y, waist_radius), (waist_right_x, waist_y, waist_radius), (hip_left_x, hip_y, hip_radius), (hip_right_x, hip_y, hip_radius))
        self.connect_polygon((waist_left_x, waist_y, -waist_radius), (waist_right_x, waist_y, -waist_radius), (hip_left_x, hip_y, -hip_radius), (hip_right_x, hip_y, -hip_radius))

        # Generate bottom (to cover the hole by the crotch)
        self.connect_polygon((hip_left_x, hip_y, hip_radius), (hip_right_x, hip_y, hip_radius), (hip_left_x, hip_y, -hip_radius), (hip_right_x, hip_y, -hip_radius))

        self.xbounds = [hip_left_x - hip_radius, hip_right_x + hip_radius]
        self.ybounds = [waist_y, hip_y]
