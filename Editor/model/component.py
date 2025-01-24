import numpy as np
import math

from modules.utils import rotation_matrix

ROTATION_SPEED = 0.03
MAX_ROTATION_ANGLE = 180 # Degrees

class Component:
    def __init__(self):
        self.MODEL_START_Y = 120
        self.center_x = 960
        self.center_y = 540
        self.polygons = []
        
    def to_rad(self, cir):
        """Converts circumference to radius"""
        return cir / (2 * math.pi)

    def generate_tube(self, top_y, bottom_y, top_x, bottom_x, top_radius, bottom_radius, num_steps=36, offset=0, color=0):
        tube = []

        for i in range(num_steps):
            i += offset
            angle = math.radians(i * 360 / 36)
            next_angle = math.radians((i + 1) * 360 / 36)

            top_left =     (top_x    + top_radius    * math.cos(angle),      top_y,    top_radius    * math.sin(angle))
            top_right =    (top_x    + top_radius    * math.cos(next_angle), top_y,    top_radius    * math.sin(next_angle))
            bottom_left =  (bottom_x + bottom_radius * math.cos(angle),      bottom_y, bottom_radius * math.sin(angle))
            bottom_right = (bottom_x + bottom_radius * math.cos(next_angle), bottom_y, bottom_radius * math.sin(next_angle))

            # Top left, top right, bottom left, bottom right, average z, color quadrant
            avg_z = top_left[2] + top_right[2] + bottom_left[2] + bottom_right[2]
            avg_z /= 4
            tube.append([top_left, top_right, bottom_right, bottom_left, [avg_z, 0], [color, 0]])

        return tube
    
    def generate_face(self, top_xl, bottom_xl, top_xr, bottom_xr, top_y, bottom_y, top_z, bottom_z, num_segments=8, color=0):
        dist_top = top_xr - top_xl
        dist_bottom = bottom_xr - bottom_xl
        step_top = dist_top / num_segments
        step_bottom = dist_bottom / num_segments

        face = []
        for i in range(num_segments):
            polygon = [[top_xl + step_top * (i), top_y, -top_z],
                       [top_xl + step_top * (i + 1), top_y, -top_z],
                       [bottom_xl + step_bottom * (i + 1), bottom_y, -bottom_z],
                       [bottom_xl + step_bottom * (i), bottom_y, -bottom_z],
                       [0, 0], [color, 0]]
            polygon[4][0] = (polygon[0][2] + polygon[1][2] + polygon[2][2] + polygon[3][2]) / 4

            face.append(polygon)
        return face
            

    def rotate(self, axis=[0, 1, 0], direction=1):
        """Transforms the points in this component to rotate in the given direction"""
        rotation = rotation_matrix(axis, ROTATION_SPEED * direction)

        polygons = self.polygons.copy()
        self.polygons = []

        for polygon in polygons:
            new_poly = []
            for point in polygon:
                if len(point) == 2:
                    new_poly.append(point)
                    continue
                altered_point = np.dot(rotation, [point[0] - self.center_x, point[1] - self.center_y, point[2]])
                new_poly.append([altered_point[0] + self.center_x, altered_point[1] + self.center_y, altered_point[2]])
            self.polygons.append(new_poly)