import pygame as pyg

from classes.display import Colors

from Editor.components.component_base import ModelComponent

class Bust(ModelComponent):
    def __init__(self):
        super().__init__()

    def generate_model_data(self, components, measurements, top_y):
        super().generate_model_data()

        # self.generate_semispheres(components, measurements, top_y)
        self.generate_triangle(components, measurements, top_y)

    def generate_triangle(self, components, measurements, top_y):
        # Get lc points
        lc_radius = measurements["low_chest_depth"] / 2
        lc_left_x  = self.center_x - measurements["low_chest_width"] / 2
        lc_right_x = self.center_x + measurements["low_chest_width"] / 2
        lc_y = top_y + measurements["shldr_to_lowchest"]

        # Get uc points
        uc_radius = measurements["up_chest_depth"] / 2
        shoulder_top_x    = self.center_x - (measurements["shoulder_width"] - uc_radius) / 2
        shoulder_bottom_x = self.center_x - (measurements["shoulder_width"] - uc_radius) / 2 
        shoulder_height   = ((shoulder_top_x - shoulder_bottom_x) ** 2 + (self.ctw(measurements["armh_cir"])) ** 2) ** 0.5
        uc_y = top_y + shoulder_height
        uc_left_x  = self.center_x - (measurements["up_chest_width"] - uc_radius) / 2
        uc_right_x = self.center_x + (measurements["up_chest_width"] - uc_radius) / 2
        
        # Get bp height
        nipple_z = measurements["mid_chest_depth"] - measurements["low_chest_depth"] / 2
        # nipple_y = top_y + (measurements["high_pt"] ** 2 - nipple_z ** 2) ** 0.5
        nipple_y = top_y + measurements["high_pt"]
        self.nipple_y = nipple_y

        # Generate left/right sides
        self.connect_polygon((lc_left_x - lc_radius / 2, lc_y, lc_radius), (lc_left_x - lc_radius / 2, lc_y, lc_radius), (uc_left_x - uc_radius, nipple_y, nipple_z), (uc_left_x - uc_radius, uc_y, uc_radius))
        self.connect_polygon((lc_right_x + lc_radius / 2, lc_y, lc_radius), (lc_right_x + lc_radius / 2, lc_y, lc_radius), (uc_right_x + uc_radius, nipple_y, nipple_z), (uc_right_x + uc_radius, uc_y, uc_radius))
        self.connect_polygon((lc_left_x - lc_radius / 2, lc_y, lc_radius), (lc_left_x - lc_radius / 2, lc_y, 0), (uc_left_x - uc_radius, uc_y, uc_radius), (uc_left_x - uc_radius, uc_y, 0))
        self.connect_polygon((lc_right_x + lc_radius / 2, lc_y, lc_radius), (lc_right_x + lc_radius / 2, lc_y, 0), (uc_right_x + uc_radius, uc_y, uc_radius), (uc_right_x + uc_radius, uc_y, 0))

        # # Generate top/bottom 
        self.connect_polygon((lc_left_x - lc_radius / 2, lc_y, lc_radius), (lc_right_x + lc_radius / 2, lc_y, lc_radius), (uc_left_x - uc_radius, nipple_y, nipple_z), (uc_right_x + uc_radius, nipple_y, nipple_z))

        self.connect_polygon((uc_left_x - uc_radius, uc_y, uc_radius), (uc_right_x + uc_radius, uc_y, uc_radius), (uc_left_x - uc_radius, nipple_y, nipple_z), (uc_right_x + uc_radius, nipple_y, nipple_z))

        self.xbounds = [uc_left_x - uc_radius, uc_right_x + uc_radius]
        self.ybounds = [uc_y, lc_y]

        self.x_dist = -abs(uc_left_x - uc_radius - (lc_left_x - lc_radius))

    def get_hovered_point(self, surface: pyg.Surface, mouse_position):
        if pyg.key.get_pressed()[pyg.K_LCTRL]:
            return round(mouse_position[0], 2), round(mouse_position[1], 2)

        else:
            if abs(mouse_position[0] - self.center_x) < 15:
                return round(self.center_x, 2), round(mouse_position[1], 2)
            else:
                base_x = (self.xbounds[0] if mouse_position[0] < surface.get_width() / 2 else self.xbounds[1])
                if mouse_position[1] >= self.nipple_y:

                    y_ratio = (mouse_position[1] - self.nipple_y) / (self.ybounds[1] - self.nipple_y)
                    x_distance = self.x_dist * y_ratio

                    return round(base_x - (x_distance if mouse_position[0] < surface.get_width() / 2 else -x_distance), 2), round(mouse_position[1], 2)
                else:
                    return round(base_x, 2), round(mouse_position[1], 2)