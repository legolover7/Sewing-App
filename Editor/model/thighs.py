from Editor.model.component import Component

class Thighs(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def generate_model_data(self):
        self.top_y = self.parent.top_y + self.parent.measurements["shldr_to_waist"] + self.parent.measurements["waist_to_hip_len"]
        self.bottom_y = self.parent.top_y + self.parent.measurements["fbod_len"] + self.parent.measurements["waist_to_knee_len"]
        
        hip_center_xl = self.center_x + self.parent.measurements["hip_width"] / 4
        hip_center_xr = self.center_x - self.parent.measurements["hip_width"] / 4

        left_thigh = self.generate_tube(self.top_y, self.bottom_y, hip_center_xl, hip_center_xl,
                                        self.parent.measurements["hip_width"] / 4,
                                        self.to_rad(self.parent.measurements["knee_cir"]))
        right_thigh = self.generate_tube(self.top_y, self.bottom_y, hip_center_xr, hip_center_xr,
                                         self.parent.measurements["hip_width"] / 4,
                                         self.to_rad(self.parent.measurements["knee_cir"]))
        
        self.polygons = left_thigh + right_thigh