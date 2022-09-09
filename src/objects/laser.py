import pygame
from enum import Enum
from math import cos, sin

from globals import *
from utils import *

class Laser:
    SPEED = 500.0
    SIZE = 1.5
    EXPLODE_SIZE = 5.0
    EXPLODE_DUR = 0.1

    class Status(Enum):
        FIRED = 0
        EXPLODING = 1
        DESTROYED = 2

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.x_vel = self.SPEED * cos(angle)
        self.y_vel = -self.SPEED * sin(angle)
        self.travel_time = 0
        self.status = self.Status.FIRED
        self.explode_time = 0

    def draw(self, win):
        if self.status == self.Status.FIRED:
            pygame.draw.circle(win, YELLOW1, (self.x, self.y), self.SIZE)
        elif self.status == self.Status.EXPLODING:
            draw_explosion(win, ORANGE, YELLOW2, (self.x, self.y), self.EXPLODE_SIZE, self.EXPLODE_SIZE / 2)

    def move(self, dt):
        if self.status == self.Status.EXPLODING:
            self.explode_time += dt

            if self.explode_time > self.EXPLODE_DUR:
                self.status = self.Status.DESTROYED
                self.explode_time = 0
                return False

        elif self.status == self.Status.DESTROYED:
            return False

        else:
            self.x = wrap_x(self.x + self.x_vel * dt)
            self.y = wrap_y(self.y + self.y_vel * dt)
            self.travel_time += dt

        return True

    def explode(self):
        self.status = self.Status.EXPLODING