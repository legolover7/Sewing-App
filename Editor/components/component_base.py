import pygame as pyg
import numpy as np
import math

from classes.display import Colors
from classes.globals import Globals

import modules.collider as collider
from modules.utils import rotation_matrix

ROTATION_SPEED = 0.00005
MAX_ROTATION_ANGLE = 180 # Degrees

class ModelComponent:
    def __init__(self):
        self.center_x = 1920 / 2
        self.rotation = 0
        
    def generate_model_data(self):
        self.data = {
            "verticies": [],
            "points": [],
            "lines": [],
            "polygons": []
        }
        self.xbounds = [0, 0]
        self.ybounds = [0, 0]
        self.x_dist = 0
        self.add_x = False

    def render(self, surface: pyg.Surface, color):    
        if collider.collides_point(Globals.mouse_position, (self.xbounds[0], self.ybounds[0], self.xbounds[1] - self.xbounds[0], self.ybounds[1] - self.ybounds[0])):
            color = Colors.green

        for line in self.data["lines"]:
            point1 = self.data["verticies"][line[0]]
            point2 = self.data["verticies"][line[1]]
            pyg.draw.line(surface, color, point1[:2], point2[:2])
        
        for polygon in self.data["polygons"]:
            point1 = self.data["verticies"][polygon[0]]
            point2 = self.data["verticies"][polygon[1]]
            point3 = self.data["verticies"][polygon[2]]
            point4 = self.data["verticies"][polygon[3]]

            pyg.draw.polygon(surface, color, (point1[:2], point2[:2], point3[:2], point4[:2]))

        for point in self.data["points"]:
            pyg.draw.circle(surface, color, self.data["verticies"][point[0]][:2], point[1])
    
    def get_hovered_point(self, surface: pyg.Surface, mouse_position):
        if pyg.key.get_pressed()[pyg.K_LCTRL] or pyg.key.get_pressed()[pyg.K_RCTRL]:
            return round(mouse_position[0], 2), round(mouse_position[1], 2)

        else:
            if abs(mouse_position[0] - self.center_x) < 15:
                x_position = 0
            else:
                base_x = (self.xbounds[0] if mouse_position[0] < surface.get_width() / 2 else self.xbounds[1])
                if self.add_x:
                    base_x += (self.x_dist if mouse_position[0] < surface.get_width() / 2 else -self.x_dist)

                y_ratio = (mouse_position[1] - self.ybounds[0]) / (self.ybounds[1] - self.ybounds[0])
                x_distance = self.x_dist * y_ratio

                x_position = base_x - (x_distance if mouse_position[0] < surface.get_width() / 2 else -x_distance) - self.center_x

                # x_position = np.dot(rotation_matrix([0, 1, 0], self.rotation), (x_position, 0, 0))[0]

        return round(self.center_x + x_position, 2), round(mouse_position[1], 2)
    
    def rotate(self, axis=[0, 1, 0], direction=1):
        """Transforms the points in this component to rotate in the given direction"""
        rotation = rotation_matrix(axis, ROTATION_SPEED * direction)
        self.rotation += math.degrees(ROTATION_SPEED * direction)
        if abs(self.rotation) > MAX_ROTATION_ANGLE:
            if self.rotation < 0:
                self.rotation = -MAX_ROTATION_ANGLE
            else:
                self.rotation = MAX_ROTATION_ANGLE
            return

        for i, point in enumerate(self.data["verticies"]):
            altered = np.dot(rotation, (point[0] - 1920/2, point[1] - 1080/2, point[2]))
            self.data["verticies"][i] = altered[0] + 1920/2, altered[1] + 1080/2, altered[2]

    def connect_line(self, point1: tuple = (0, 0), point2: tuple = (0, 0)):
        """Connects the last two points into a line. If points are supplied, will connect those instead"""
        if point1 != (0, 0):
            self.data["verticies"].append(point1)
            self.data["verticies"].append(point2)

        start_index = len(self.data["verticies"]) - 2
        self.data["lines"].append([start_index, start_index + 1])

    def connect_polygon(self, point1=(0, 0), point2=(0, 0), point3=(0, 0), point4=(0, 0)):
        """Connects the last four points into a polygon"""
        if point1 != (0, 0):
            self.data["verticies"].append(point1)
            self.data["verticies"].append(point2)
            self.data["verticies"].append(point3)
            self.data["verticies"].append(point4)

        start_index = len(self.data["verticies"]) - 4
        p = [start_index, start_index + 1, start_index + 3, start_index + 2]
        
        self.data["polygons"].append(p)

    def generate_line(self, point1, point2):
        self.data["verticies"].append(point1)
        self.data["verticies"].append(point2)


    def generate_circle(self, x: float, y: float, radius: float):
        for i in range(32):
            if i == 8 or i == 24:
                point = (x, y, radius * (-1 if i > 16 else 1))
            else:
                theta = 11.25 * (i)
                offset_x = radius * math.cos(math.radians(theta))
                offset_z = radius * math.sin(math.radians(theta))
                point = (x + offset_x, y, offset_z)
                self.data["verticies"].append(point)

    def generate_tube(self, x1, y1, r1, x2, y2, r2, direction=0):
        """If direction is provided, it creates a semicircle in that direction"""
        start = 0
        stop = 32
        if direction == -1:
            start = 8
            stop = 25
        elif direction == 1:
            start = 24
            stop = 41
            
        for i in range(start, stop):
            if i % 32 == 8:
                point1 = (x1, y1, r1 * (-1 if i % 32 > 16 else 1))
                point2 = (x2, y2, r2 * (-1 if i % 32 > 16 else 1))
                self.data["verticies"].append(point1)
                self.data["verticies"].append(point2)
            else:
                theta = 11.25 * (i)
                offset_x1 = r1 * math.cos(math.radians(theta))
                offset_z1 = r1 * math.sin(math.radians(theta))
                offset_x2 = r2 * math.cos(math.radians(theta))
                offset_z2 = r2 * math.sin(math.radians(theta))
                point1 = (x1 + offset_x1, y1, offset_z1)
                point2 = (x2 + offset_x2, y2, offset_z2)
                self.data["verticies"].append(point1)
                self.data["verticies"].append(point2)
            if i > start:
                self.connect_polygon()

        if direction == 0:
            start_index = len(self.data["verticies"]) - 2
            p = [start_index, start_index + 1, start_index - 61, start_index - 62]
            self.data["polygons"].append(p)
                
    def ctw(self, circumference):
        """Converts a circumference of a circle to its width"""
        return circumference / math.pi