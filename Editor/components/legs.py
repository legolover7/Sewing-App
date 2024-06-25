import pygame as pyg

from Editor.components.component_base import ModelComponent

class Legs(ModelComponent):
    def __init__(self):
        super().__init__()
        self.control_points = {
            "left_hip_front": (0, 0, 0),
            "left_hip_back": (0, 0, 0),
            "right_hip_front": (0, 0, 0),
            "right_hip_back": (0, 0, 0),
            "hip_radius": 0
        }

    def generate_model_data(self, components, measurements, top_y):
        super().generate_model_data()
        # Right upper leg
        hip_center_x = self.center_x - measurements["hip_width"] / 4
        hip_center_y = top_y + measurements["fbod_len"] + measurements["waist_to_hip_len"]

        knee_center_y = top_y + measurements["fbod_len"] + measurements["waist_to_knee_len"]
        self.generate_tube(hip_center_x, hip_center_y, measurements["hip_width"] / 4, hip_center_x, knee_center_y, self.ctw(measurements["knee_cir"]) / 2)

        hip_radius = measurements["hip_width"] / 4
        self.control_points["right_hip_front"] = (hip_center_x, hip_center_y, -hip_radius)
        self.control_points["right_hip_back"] = (hip_center_x, hip_center_y, hip_radius)
        self.xbounds[0] = hip_center_x - hip_radius

        self.radius = hip_radius

        # Left upper leg
        hip_center_x = self.center_x + measurements["hip_width"] / 4
        self.generate_tube(hip_center_x, hip_center_y, measurements["hip_width"] / 4, hip_center_x, knee_center_y, self.ctw(measurements["knee_cir"]) / 2)
        
        self.control_points["left_hip_front"] = (hip_center_x, hip_center_y, -hip_radius)
        self.control_points["left_hip_back"] = (hip_center_x, hip_center_y, hip_radius)

        self.xbounds[1] = hip_center_x + hip_radius
        self.ybounds = [hip_center_y, knee_center_y]

        self.x_dist = -abs(hip_center_x - hip_radius - (hip_center_x - self.ctw(measurements["knee_cir"]) / 2))

    def get_hovered_point(self, surface: pyg.Surface, mouse_position):
        if pyg.key.get_pressed()[pyg.K_LCTRL]:
            return round(mouse_position[0], 2), round(mouse_position[1], 2)

        else:
            invert = False
            if mouse_position[0] < surface.get_width() / 2:
                if mouse_position[0] - self.xbounds[0] > self.radius:
                    base_x = self.xbounds[0] + self.radius * 2
                    invert = True
                else:
                    base_x = self.xbounds[0]
            else:
                if self.xbounds[1] - mouse_position[0] > self.radius:
                    base_x = self.xbounds[1] - self.radius * 2
                    invert = True
                else:
                    base_x = self.xbounds[1]

            y_ratio = (mouse_position[1] - self.ybounds[0]) / (self.ybounds[1] - self.ybounds[0])
            x_distance = self.x_dist * y_ratio

            if invert:
                x_distance *= -1

            return round(base_x - (x_distance if mouse_position[0] < surface.get_width() / 2 else -x_distance), 2), round(mouse_position[1], 2)