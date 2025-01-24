from Editor.model.component import Component

class LChest(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def generate_model_data(self):
        self.top_y = self.parent.top_y + self.parent.measurements["shldr_to_lowchest"]
        self.bottom_y = self.parent.top_y + self.parent.measurements["shldr_to_waist"]

        lowchest_rad = self.parent.measurements["low_chest_depth"] / 2

        lowchest_xl = self.center_x + (self.parent.measurements["low_chest_width"] - lowchest_rad) / 2
        lowchest_xr = self.center_x - (self.parent.measurements["low_chest_width"] - lowchest_rad) / 2
        waist_xl = self.center_x + self.parent.measurements["waist_width"] * 3 / 8
        waist_xr = self.center_x - self.parent.measurements["waist_width"] * 3 / 8

        left_side = self.generate_tube(self.top_y, self.bottom_y, lowchest_xl, waist_xl,
                           lowchest_rad,
                           self.parent.measurements["waist_width"] / 4, 18, 27)

        right_side = self.generate_tube(self.top_y, self.bottom_y, lowchest_xr, waist_xr,
                           lowchest_rad,
                           self.parent.measurements["waist_width"] / 4, 18, 9)
        
        back_face = self.generate_face(lowchest_xl, waist_xl, lowchest_xr, waist_xr, 
                                       self.top_y, self.bottom_y, 
                                       self.parent.measurements["waist_width"] / 4, 
                                       self.parent.measurements["waist_width"] / 4)
        front_face = self.generate_face(lowchest_xl, waist_xl, lowchest_xr, waist_xr, 
                                        self.top_y, self.bottom_y, 
                                        -self.parent.measurements["waist_width"] / 4, 
                                        -self.parent.measurements["waist_width"] / 4)
        
        self.polygons = left_side + right_side + back_face + front_face
