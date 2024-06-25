from Editor.components.component_base import ModelComponent

class Shoulders(ModelComponent):
    def __init__(self):
        super().__init__()
    
    def generate_model_data(self, components, measurements, top_y):
        super().generate_model_data()

        # Get radii
        shoulder_radius = measurements["up_chest_depth"] / 2
        uc_radius = measurements["up_chest_depth"] / 2

        # Shoulder calculations to figure out shoulder height
        shoulder_top_x    = self.center_x - (measurements["shoulder_width"] - shoulder_radius) / 2
        shoulder_bottom_x = self.center_x - (measurements["shoulder_width"] - shoulder_radius) / 2 
        shoulder_height   = ((shoulder_top_x - shoulder_bottom_x) ** 2 + (self.ctw(measurements["armh_cir"])) ** 2) ** 0.5

        # Get x values
        shoulder_left_x  = self.center_x - measurements["shoulder_width"] / 2
        shoulder_right_x = self.center_x + measurements["shoulder_width"] / 2
        uc_left_x        = self.center_x - (measurements["up_chest_width"] - uc_radius) / 2
        uc_right_x       = self.center_x + (measurements["up_chest_width"] - uc_radius) / 2

        # Get y values
        shoulder_y = top_y
        uc_y       = top_y + shoulder_height
        
        # Generate sides
        self.generate_tube(shoulder_left_x, shoulder_y, shoulder_radius, uc_left_x, uc_y, uc_radius, -1)
        self.generate_tube(shoulder_right_x, shoulder_y, shoulder_radius, uc_right_x, uc_y, uc_radius, 1)

        # Generate front/back
        self.connect_polygon((shoulder_left_x, shoulder_y, shoulder_radius), (shoulder_right_x, shoulder_y, shoulder_radius), (uc_left_x, uc_y, uc_radius), (uc_right_x, uc_y, uc_radius))
        self.connect_polygon((shoulder_left_x, shoulder_y, -shoulder_radius), (shoulder_right_x, shoulder_y, -shoulder_radius), (uc_left_x, uc_y, -uc_radius), (uc_right_x, uc_y, -uc_radius))

        self.xbounds = [shoulder_left_x - shoulder_radius, shoulder_right_x + shoulder_radius]
        self.ybounds = [shoulder_y, uc_y]

        self.x_dist = -abs(shoulder_left_x - shoulder_radius - (uc_left_x - uc_radius))