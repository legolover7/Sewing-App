from Editor.model.component import Component

class LLegs(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def generate_model_data(self):
        self.top_y = self.parent.top_y + self.parent.measurements["shldr_to_waist"] + self.parent.measurements["waist_to_knee_len"]
        self.bottom_y = self.parent.top_y + self.parent.measurements["shoulder_height"] - self.parent.measurements["ankle_height"]

        knee_center_xl = self.center_x + self.parent.measurements["hip_width"] / 4
        knee_center_xr = self.center_x - self.parent.measurements["hip_width"] / 4

        lower_left_leg = self.generate_tube(self.top_y, self.bottom_y, knee_center_xl, knee_center_xl, 
                           self.to_rad(self.parent.measurements["knee_cir"]), 
                           self.to_rad(self.parent.measurements["ankle_cir"]))
        lower_right_leg = self.generate_tube(self.top_y, self.bottom_y, knee_center_xr, knee_center_xr, 
                           self.to_rad(self.parent.measurements["knee_cir"]), 
                           self.to_rad(self.parent.measurements["ankle_cir"]))

        self.polygons = lower_left_leg + lower_right_leg