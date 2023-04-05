import math
from typing import Union
import pygame
from Transformable import Transformable


class Camera(Transformable):
    def __init__(self, screen: pygame.Surface, car: Union[Transformable, None] = None):
        super().__init__()
        self.car = car
        self.screen = screen

    def get_coord(self, x: float, y: float) -> tuple[float, float]:
        center = self.screen.get_rect().center

        x -= self.x
        y -= self.y

        x, y = x * math.cos(self.rot) - y * math.sin(self.rot), x * math.sin(self.rot) + y * math.cos(self.rot)

        return x + center[0], y + center[1]

    def update(self, dt: float):
        if self.car is None:
            if pygame.key.get_pressed()[pygame.K_w]:
                self.translate_forward(-500 * dt)
            if pygame.key.get_pressed()[pygame.K_s]:
                self.translate_forward(500 * dt)
            if pygame.key.get_pressed()[pygame.K_a]:
                self.translate(-500 * dt, 0)
            if pygame.key.get_pressed()[pygame.K_d]:
                self.translate(500 * dt, 0)
            return

        self.x = self.car.x
        self.y = self.car.y
        self.rot = self.car.rot
