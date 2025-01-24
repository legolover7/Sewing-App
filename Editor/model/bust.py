from classes.display import Colors

from Editor.model.component import Component

class Bust(Component):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def generate_model_data(self):
        upchest_rad = self.parent.measurements["up_chest_depth"] / 2
        lowchest_rad = self.parent.measurements["low_chest_depth"] / 2

        upchest_xl = self.center_x + (self.parent.measurements["shoulder_width"] - upchest_rad) / 2 + upchest_rad 
        upchest_xr = self.center_x - (self.parent.measurements["shoulder_width"] - upchest_rad) / 2 - upchest_rad
        lowchest_xl = self.center_x + (self.parent.measurements["low_chest_width"] - lowchest_rad) / 2 + lowchest_rad
        lowchest_xr = self.center_x - (self.parent.measurements["low_chest_width"] - lowchest_rad) / 2 - lowchest_rad

        # Get lc points
        lowchest_y = self.parent.top_y + self.parent.measurements["shldr_to_lowchest"]

        # Get uc points
        shoulder_xr = self.center_x - self.parent.measurements["shoulder_width"] * 5 / 8
        x_displacement = shoulder_xr - (self.center_x - (self.parent.measurements["shoulder_width"] - upchest_rad) / 2 )
        y_displacement = ((self.to_rad(self.parent.measurements["armh_cir"]) * 2) ** 2 - x_displacement ** 2) ** 0.5

        upchest_y = self.parent.top_y + y_displacement
        
        # Get bp height
        nipple_z = self.parent.measurements["mid_chest_depth"] / 2
        nipple_y = self.parent.top_y + (self.parent.measurements["high_pt"] ** 2 - nipple_z ** 2) ** 0.5
        self.nipple_y = nipple_y

        # Generate left/right sides
        midchest_xl = (lowchest_xl + upchest_xl) / 2 + 3
        midchest_xr = (lowchest_xr + upchest_xr) / 2 - 3
        self.polygons.append([[lowchest_xl, lowchest_y, -lowchest_rad],
                             [lowchest_xl, lowchest_y, -0],  
                             [midchest_xl, nipple_y, 0],
                             [upchest_xl, nipple_y, -nipple_z], [0, 0], [Colors.gray4, 0]])
        self.polygons.append([[upchest_xl, upchest_y, -lowchest_rad],
                             [upchest_xl, upchest_y, -0],  
                             [midchest_xl, nipple_y, 0],
                             [upchest_xl, nipple_y, -nipple_z], [0, 0], [Colors.gray3, 0]])
        self.polygons.append([[lowchest_xr, lowchest_y, -lowchest_rad],
                             [lowchest_xr, lowchest_y, -0],  
                             [midchest_xr, nipple_y, 0],
                             [upchest_xr, nipple_y, -nipple_z], [0, 0], [Colors.gray4, 0]])
        self.polygons.append([[upchest_xr, upchest_y, -lowchest_rad],
                             [upchest_xr, upchest_y, -0],  
                             [midchest_xr, nipple_y, 0],
                             [upchest_xr, nipple_y, -nipple_z], [0, 0], [Colors.gray3, 0]])

        # Generate top/bottom 
        self.polygons += self.generate_face(upchest_xl, lowchest_xl, upchest_xr, lowchest_xr, nipple_y, lowchest_y, nipple_z, lowchest_rad, 64, Colors.gray3)
        self.polygons += self.generate_face(upchest_xl, upchest_xl, upchest_xr, upchest_xr, upchest_y, nipple_y, upchest_rad, nipple_z, 64, Colors.gray4)
        
        for polygon in self.polygons:
            if polygon[4][0] == 0:
                polygon[4][0] = (polygon[0][2] + polygon[1][2] + polygon[2][2] + polygon[3][2]) / 4
            else:
                polygon[4][0] = nipple_z