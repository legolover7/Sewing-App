from Editor.model.component import Component

class UChest(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def generate_model_data(self):
        upchest_rad = self.parent.measurements["up_chest_depth"] / 2
        lowchest_rad = self.parent.measurements["low_chest_depth"] / 2

        upchest_xl = self.center_x + (self.parent.measurements["shoulder_width"] - upchest_rad) / 2 
        upchest_xr = self.center_x - (self.parent.measurements["shoulder_width"] - upchest_rad) / 2 
        lowchest_xl = self.center_x + (self.parent.measurements["low_chest_width"] - lowchest_rad) / 2
        lowchest_xr = self.center_x - (self.parent.measurements["low_chest_width"] - lowchest_rad) / 2

        # Figure out shoulder height
        shoulder_top_x    = self.center_x - self.parent.measurements["shoulder_width"] * 5 / 8
        x_displacement = shoulder_top_x - upchest_xr
        y_displacement = ((self.to_rad(self.parent.measurements["armh_cir"]) * 2) ** 2 - x_displacement ** 2) ** 0.5
        
        self.top_y = self.parent.top_y + y_displacement
        self.bottom_y = self.parent.top_y + self.parent.measurements["shldr_to_lowchest"]

        left_side = self.generate_tube(self.top_y, self.bottom_y, upchest_xl, lowchest_xl,
                           upchest_rad,
                           lowchest_rad, 18, 27)

        right_side = self.generate_tube(self.top_y, self.bottom_y, upchest_xr, lowchest_xr,
                           upchest_rad,
                           lowchest_rad, 18, 9)
        
        self.polygons = left_side + right_side
        
        self.polygons += self.generate_face(upchest_xl, lowchest_xl, upchest_xr, lowchest_xr, self.top_y, self.bottom_y, upchest_rad, lowchest_rad, 64)
        self.polygons += self.generate_face(upchest_xl, lowchest_xl, upchest_xr, lowchest_xr, self.top_y, self.bottom_y, -upchest_rad, -lowchest_rad, 8)