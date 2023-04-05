import BezierCurve as bc
from Camera import Camera
import pygame
import pyclipper


class Track:
    def __init__(self, track_name: str, width: int, scale: int = 5):
        with open(track_name, 'r') as f:
            self.curve = bc.BezierCurve.deserialize(f.read())
        self.curve.pts = [p.translated(-self.curve.pts[0].x, -self.curve.pts[0].y).scaled(scale) for p in self.curve.pts]
        self.width = width
        self.polyline_factor = 0.05

        self.polyline = self.curve.get_polyline(self.polyline_factor)

        pco = pyclipper.PyclipperOffset()
        pco.AddPath(self.polyline, pyclipper.JT_ROUND, pyclipper.ET_OPENROUND)
        self.polygon = pco.Execute(self.width)[0]

    def draw(self, screen: pygame.Surface, color: pygame.Color, camera: Camera, width: int = 1):
        pygame.draw.polygon(screen, color, [camera.get_coord(x, y) for x, y in self.polygon], width)
