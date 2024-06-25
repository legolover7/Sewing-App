import pygame as pyg
import numpy as np
import math

from classes.display import Colors
from classes.globals import Globals

from Editor.components.component_base import ModelComponent, ROTATION_SPEED, MAX_ROTATION_ANGLE
from Editor.components.abdomen import Abdomen
from Editor.components.bust import Bust
from Editor.components.chest import Chest
from Editor.components.lower_chest import LowerChest
from Editor.components.legs import Legs
from Editor.components.lower_legs import LowerLegs
from Editor.components.shoulders import Shoulders

import modules.collider as collider
import modules.utils as utils

class Model:
    def __init__(self):
        self.display = pyg.Surface((1920, 1080))
        self.components: list[ModelComponent] = [
            LowerLegs(),
            Legs(),
            Abdomen(),
            LowerChest(),
            Chest(),
            Bust(),
            Shoulders()
        ]
        self.measurements = {}
        self.clothes_data = {}
        self.type = "F"
        self.model_hovered = False
        self.rotation = 0

        self.edit_mode = "none"

        # Colors for model segments
        start = 40
        dist = 205 - start
        self.model_colors = []
        for i in range(len(self.components)):
            c = start + i * (dist / len(self.components))
            self.model_colors.append((c, c, c))

    def load(self):
        self.model_height = self.measurements["height"]
        self.model_width = self.measurements["shoulder_width"]
        self.raw_data = self.measurements.copy()

        # If model height is 70 units, for instance, one unit will equate to ~14.28 pixels
        # Enables any measurement to be used, as it's just based on ratios
        # 1000px height allows for padding of 40px on both top and bottom
        self.ratio = 980 / self.model_height

        # Convert everything to pixel measurements
        for m in self.measurements:
            self.measurements[m] *= self.ratio

    def create_model(self):
        self.clothes_data = {
            "verticies": [],
            "lines": []
        }
        top_y = self.model_height * self.ratio - (self.measurements["skirt_len"] + self.measurements["fbod_len"]) + 40

        for component in self.components:
            component.generate_model_data(self.components, self.measurements, top_y)
            # print(type(component), len(component.data["verticies"]), len(component.data["polygons"]))

    def rotate_components(self, axis, direction):
        for component in self.components:
            component.rotate(axis, direction)

        # Rotate clothes verticies
        rotation = utils.rotation_matrix(axis, ROTATION_SPEED * direction)
        self.rotation += math.degrees(ROTATION_SPEED * direction)
        if abs(self.rotation) > MAX_ROTATION_ANGLE:
            if self.rotation < 0:
                self.rotation = -MAX_ROTATION_ANGLE
            else:
                self.rotation = MAX_ROTATION_ANGLE
            return
        
        for i, point in enumerate(self.clothes_data["verticies"]):
            altered = np.dot(rotation, (point[0] - 1920/2, point[1] - 1080/2, point[2]))
            self.clothes_data["verticies"][i] = altered[0] + 1920/2, altered[1] + 1080/2, altered[2]


    def draw_model(self, highlight_segments):
        """Draws the model, using Z indicies to determine which sections to show"""
        self.display.fill(Colors.charcoal)

        polygons = {}
        
        for i, component in enumerate(self.components):
            # component.render(self.display, self.model_colors[i])
            for polygon in component.data["polygons"]:
                point1 = component.data["verticies"][polygon[0]]
                point2 = component.data["verticies"][polygon[1]]
                point3 = component.data["verticies"][polygon[2]]
                point4 = component.data["verticies"][polygon[3]]

                # Get average Z index
                z = round((point1[2] + point2[2] + point3[2] + point4[2]) / 4)

                # Add to the dictionary
                if collider.collides_point(Globals.mouse_position, (component.xbounds[0], component.ybounds[0], component.xbounds[1] - component.xbounds[0], component.ybounds[1] - component.ybounds[0])) and highlight_segments:
                    color = Colors.green
                else:
                    color = self.model_colors[i]

                if z in polygons:
                    polygons[z].append((point1[:2], point2[:2], point3[:2], point4[:2], color))
                else:
                    polygons[z] = [(point1[:2], point2[:2], point3[:2], point4[:2], color)]

        # Sort the order to draw in
        sorted_keys = sorted(list(polygons.keys()))
        for key in sorted_keys:
            for polygon in polygons[key]:
                pyg.draw.polygon(self.display, polygon[4], polygon[:4])

        # Get hovered point
        if self.edit_mode != "none":
            self.model_hovered = False
            for component in self.components:
                if isinstance(component, Chest):
                    continue
                
                if collider.collides_point(Globals.mouse_position, (component.xbounds[0], component.ybounds[0], component.xbounds[1] - component.xbounds[0], component.ybounds[1] - component.ybounds[0])):
                    self.hovered_point = component.get_hovered_point(self.display, Globals.mouse_position)
                    self.model_hovered = True

                    if pyg.key.get_pressed()[pyg.K_LSHIFT] and len(self.clothes_data["verticies"]):
                        self.hovered_point = (1920 / 2 + (1920 / 2 - self.clothes_data["verticies"][-1][0]), self.clothes_data["verticies"][-1][1])

                    # Check if the user is hovering another point
                    for point in self.clothes_data["verticies"]:
                        if utils.distance(point, Globals.mouse_position) < 5:
                            self.hovered_point = (point[0], point[1])

                    self.hovered_point = (self.hovered_point[0], self.hovered_point[1], 0)

        # Draw shirt data
        for point in self.clothes_data["verticies"]:
            pyg.draw.circle(self.display, Colors.blue, point[:2], 5)
            
        for line in self.clothes_data["lines"]:
            pyg.draw.line(self.display, Colors.blue, self.clothes_data["verticies"][line[0]][:2], self.clothes_data["verticies"][line[1]][:2])

        if self.model_hovered and self.edit_mode != "none":
            pyg.draw.circle(self.display, Colors.aqua, self.hovered_point[:2], 5)

    def add_point(self):
        self.clothes_data["verticies"].append(self.hovered_point)

    def add_line(self):
        index = len(self.clothes_data["verticies"])
        self.clothes_data["verticies"].append(self.hovered_point)
        self.clothes_data["lines"].append((index - 1, index))

    def render(self, surface: pyg.Surface, highlight_segments=True):
        self.draw_model(highlight_segments)
        surface.blit(self.display, (0, 0))