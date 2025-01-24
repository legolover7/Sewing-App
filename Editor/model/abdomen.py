from Editor.model.component import Component

class Abdomen(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def generate_model_data(self):
        self.top_y = self.parent.top_y + self.parent.measurements["shldr_to_waist"]
        self.bottom_y = self.parent.top_y + self.parent.measurements["shldr_to_waist"] + self.parent.measurements["waist_to_hip_len"]

        waist_xl = self.center_x + self.parent.measurements["waist_width"] * 3 / 8
        waist_xr = self.center_x - self.parent.measurements["waist_width"] * 3 / 8
        hip_center_xl = self.center_x + self.parent.measurements["hip_width"] / 4
        hip_center_xr = self.center_x - self.parent.measurements["hip_width"] / 4

        left_side = self.generate_tube(self.top_y, self.bottom_y, waist_xl, hip_center_xl,
                           self.parent.measurements["waist_width"] / 4,
                           self.parent.measurements["hip_width"] / 4, 18, 27)

        right_side = self.generate_tube(self.top_y, self.bottom_y, waist_xr, hip_center_xr,
                           self.parent.measurements["waist_width"] / 4,
                           self.parent.measurements["hip_width"] / 4, 18, 9)

        back_face = self.generate_face(waist_xl, hip_center_xl, waist_xr, hip_center_xr, 
                                       self.top_y, self.bottom_y, 
                                       self.parent.measurements["waist_width"] / 4, 
                                       self.parent.measurements["hip_width"] / 4)
        front_face = self.generate_face(waist_xl, hip_center_xl, waist_xr, hip_center_xr, 
                                        self.top_y, self.bottom_y, 
                                        -self.parent.measurements["waist_width"] / 4, 
                                        -self.parent.measurements["hip_width"] / 4)

        self.polygons = left_side + right_side + back_face + front_face