import pygame
from math import ceil, floor, pi, radians, sin, cos
from random import randint, random
from components.sfx import Sfx

from globals import *
from utils import *

class Asteroid:
    SIZE = 100.0
    MIN_SIZE = 35.0
    MAX_SPAWN = 2
    VERT_COUNT = 10
    JAG_AMOUNT = 0.4

    def __init__(self, sfx: Sfx, x, y, *,
                 size = SIZE,
                 level = 1,
                 score = 10):

        vert = floor(randint(1, self.VERT_COUNT + 1) + self.VERT_COUNT / 2)
        offset = []
        for _ in range(vert + 1):
            offset.append(self.JAG_AMOUNT * (2 * random() - 1) + 1)

        speed = randint(1, 50) + level * 2

        self.sfx = sfx
        self.x = x
        self.y = y
        self.x_vel = random() * speed * rand_sign()
        self.y_vel = random() * speed * rand_sign()
        self.size = size
        self.level = level
        self.radius = ceil(size / 2)
        self.angle = radians(randint(1, 360))
        self.vert = vert
        self.offset = offset
        self.score = score

    def draw(self, win, debugging):
        x, y, r, o_0, a = self.x, self.y, self.radius, self.offset[0], self.angle
        points = [(
            x + r * o_0 * cos(a),
            y + r * o_0 * sin(a)
        )]
        for i, o_i in enumerate(self.offset[1:], 1):
            points.append((
                x + r * o_i * cos(a + i * pi * 2 / self.vert),
                y + r * o_i * sin(a + i * pi * 2 / self.vert)
            ))

        if debugging:
            draw_hitbox(win, RED, (x, y), r, DEBUG_WIDTH)
        draw_polygon(win, GRAY, points, SHAPE_WIDTH)

    def move(self, dt):
        self.x = wrap_x(self.x + self.x_vel * dt, self.radius)
        self.y = wrap_y(self.y + self.y_vel * dt, self.radius)

    def spawn_debris(self):
        spawn = []

        new_size = self.size * 0.6
        if new_size > self.MIN_SIZE:
            new_score = 15 if self.score < 15 else 20
            for _ in range(self.MAX_SPAWN):
                spawn.append(Asteroid(self.sfx, self.x, self.y, size = new_size, level = self.level, score = new_score))

        return spawn