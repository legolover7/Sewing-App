from Editor.model.component import Component

class Shoulders(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def generate_model_data(self):
        upchest_rad = self.parent.measurements["up_chest_depth"] / 2
        shoulder_rad = self.parent.measurements["shoulder_width"] / 8

        upchest_xl = self.center_x + (self.parent.measurements["shoulder_width"] - upchest_rad) / 2 
        upchest_xr = self.center_x - (self.parent.measurements["shoulder_width"] - upchest_rad) / 2
        shoulder_xl = self.center_x + self.parent.measurements["shoulder_width"] * 5 / 8
        shoulder_xr = self.center_x - self.parent.measurements["shoulder_width"] * 5 / 8

        # Figure out shoulder height
        x_displacement = shoulder_xr - upchest_xr
        y_displacement = ((self.to_rad(self.parent.measurements["armh_cir"]) * 2) ** 2 - x_displacement ** 2) ** 0.5
        
        self.top_y = self.parent.top_y
        self.bottom_y = self.parent.top_y + y_displacement

        left_side = self.generate_tube(self.top_y, self.bottom_y, shoulder_xl, upchest_xl,
                                       shoulder_rad, upchest_rad, 18, 27)

        right_side = self.generate_tube(self.top_y, self.bottom_y, shoulder_xr, upchest_xr,
                                        shoulder_rad, upchest_rad, 18, 9)
        
        back_face = self.generate_face(shoulder_xl, upchest_xl, shoulder_xr, upchest_xr, 
                                       self.top_y, self.bottom_y, shoulder_rad, upchest_rad)
        front_face = self.generate_face(shoulder_xl, upchest_xl, shoulder_xr, upchest_xr, 
                                        self.top_y, self.bottom_y, -shoulder_rad, -upchest_rad)
        
        self.polygons = left_side + right_side + back_face + front_face

        return