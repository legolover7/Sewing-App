import shapely.geometry as shgeo
import pygame as pyg

from classes.display import Colors

from Editor.model.component import Component
from Editor.model.abdomen import Abdomen
from Editor.model.bust import Bust
from Editor.model.upper_chest import UChest
from Editor.model.lower_chest import LChest
from Editor.model.thighs import Thighs
from Editor.model.lower_legs import LLegs
from Editor.model.shoulders import Shoulders

import modules.collider as collider

MODEL_PADDING = 50

class Model:
    def __init__(self):
        self.display = pyg.Surface((1920, 1080))
        self.model: list[Component] = [
            LLegs(self),
            Thighs(self),
            Abdomen(self),
            LChest(self),
            UChest(self),
            Bust(self),
            Shoulders(self)
        ]
        self.measurements = {}
        self.clothes_data = {}
        self.rotation = 0
        self.model_hovered = False
        self.highlight_model = False

        self.type = "F"
        self.edit_mode = "none"

        # Colors for model segments
        start = 40
        dist = 205 - start
        self.model_colors = []
        for i in range(len(self.model)):
            c = start + i * (dist / len(self.model))
            self.model_colors.append((c, c, c))

    def setup(self):
        self.full_height = self.measurements["height"]
        self.model_height = self.measurements["shoulder_height"]
        self.model_width = self.measurements["shoulder_width"]
        self.raw_data = self.measurements.copy()

        # If model height is 70 units, for instance, one unit will equate to ~14.28 pixels
        # Enables any measurement to be used, as it's just based on ratios
        # 980px height allows for padding of 50px on both top and bottom
        self.ratio = (1080 - MODEL_PADDING * 2) / self.full_height
        self.model_height *= self.ratio

        # Convert everything to pixel measurements
        for m in self.measurements:
            self.measurements[m] *= self.ratio

    def create_model(self):
        self.top_y = (1080 - MODEL_PADDING * 1.5) - self.model_height

        for component in self.model:
            component.polygons = []
            component.generate_model_data()

    def rotate_model(self, axis, direction):
        for component in self.model:
            component.rotate(axis, direction)

    def render(self, surface: pyg.Surface):
        """Renders the model, sorting by z depth"""
        self.display.fill(Colors.charcoal)

        # Collect all polygons into one list
        self.polygons = []
        for i, component in enumerate(self.model):
            if self.type != "F" and isinstance(component, Bust):
                continue
            for polygon in component.polygons:
                if polygon[5][0] == 0:
                    polygon[5][0] = self.model_colors[i]
            self.polygons += component.polygons

        # Sort polygons by depth
        for polygon in self.polygons:
            polygon[4][0] = (polygon[0][2] + polygon[1][2] + polygon[2][2] + polygon[3][2]) / 4
        self.polygons.sort(key=lambda polygon: polygon[4][0], reverse=True)

        # Search for hovered polygons
        hovered_polygon = False
        for i in range(len(self.polygons) - 1, 0, -1):
            polygon = self.polygons[i]
            if not hovered_polygon and collider.collides_point_polygon(pyg.mouse.get_pos(), polygon):
                self.polygons[i][5][1] = True
                hovered_polygon = True
            else:
                self.polygons[i][5][1] = False

        # Render polygons
        for polygon in self.polygons:
            polygon = [(point[0], point[1]) for point in polygon]
            color = polygon[5][0] if not polygon[5][1] else Colors.green
            pyg.draw.polygon(surface, color, (polygon[0], polygon[1], polygon[2], polygon[3]))
        pyg.draw.line(surface, Colors.gray2, (959, self.top_y), (959, self.top_y + self.measurements["shoulder_height"]))