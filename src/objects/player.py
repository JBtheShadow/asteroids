from typing import List
import pygame
from enum import Enum
from math import pi, radians, sin, cos

from globals import *
from utils import *
from utils import draw_big_explosion, draw_hitbox, draw_polygon, draw_ship_shape
from objects.laser import Laser

class Player:
    SHIP_SIZE = 30.0
    EXPLODE_DUR = 1.0
    VIEW_ANGLE = radians(90)
    LASER_LIMIT = 3.0
    LASER_TIMER =  1.5
    STARTING_LIVES = 3

    class Status(Enum):
        ALIVE = 0
        EXPLODING = 1

    def __init__(self, lives = STARTING_LIVES):
        self.x = WIN_WIDTH / 2.0
        self.y = WIN_HEIGHT / 2.0
        self.radius = self.SHIP_SIZE / 2.0
        self.angle = self.VIEW_ANGLE
        self.rotation = 0.0
        self.lasers : List[Laser] = []
        self.thrusting = False
        self.thrust_x = 0.0
        self.thrust_y = 0.0
        self.thrust_speed = 5.0
        self.thrust_big_flame = False
        self.thrust_flame = 2.0
        self.status = self.Status.ALIVE
        self.explode_time = 0
        self.lives = lives

    def draw_flame_thrust(self, win, fill_type, color):
        width = 2 if fill_type == "line" else 0

        x, y, r, flame = self.x, self.y, self.radius, self.thrust_flame
        si, co = sin(self.angle), cos(self.angle)

        points = [
            (x - (2/3 * co + 0.5 * si) * r, y + (2/3 * si - 0.5 * co) * r),
            (x - r * flame * co,           y + r * flame * si),
            (x - (2/3 * co - 0.5 * si) * r, y + (2/3 * si + 0.5 * co) * r),
            (x - 1/2 * co * r,              y + 1/2 * si * r)
        ]
        draw_polygon(win, color, points, width)

    def draw(self, win, dt, debugging):
        if self.status == self.Status.ALIVE:
            if self.thrusting:
                if not self.thrust_big_flame:
                    self.thrust_flame -= 10 * dt

                    if self.thrust_flame < 1.5:
                        self.thrust_big_flame = True
                else:
                    self.thrust_flame += 10 * dt

                    if self.thrust_flame > 2.5:
                        self.thrust_big_flame = False
                
                self.draw_flame_thrust(win, "fill", THRUST_YELLOW)
                self.draw_flame_thrust(win, "line", THRUST_ORANGE)

            draw_ship_shape(win, self.x, self.y, self.radius, self.angle, WHITE, 2, debugging)
        elif self.status == self.status.EXPLODING:
            draw_big_explosion(win, EXPLOSION_RED, EXPLOSION_ORANGE, EXPLOSION_YELLOW, (self.x, self.y), self.radius * 1.5, self.radius, self.radius * 0.5)

        for laser in self.lasers:
            laser.draw(win)

        if debugging:
            draw_hitbox(win, GREEN, (self.x, self.y), self.radius, 1)

    def draw_lives(self, win, debugging):
        x_pos, x_offset, y_pos = 60, 20, 25

        if self.lives > 0:
            color = GREEN
            for i in range(1, self.lives + 1):
                if i == self.lives:
                    if self.status == self.Status.EXPLODING:
                        color = HURT_RED
                    elif self.lives == 1:
                        color = WARNING_ORANGE
                draw_ship_shape(win, x_pos + x_offset * i, y_pos, self.radius / 2, self.VIEW_ANGLE, color, 1, debugging)

    def shoot(self):
        if len(self.lasers) < self.LASER_LIMIT and self.status == self.Status.ALIVE:
            self.lasers.append(Laser(self.x, self.y, self.angle))
    
    def respawn(self):
        self.lives = self.lives - 1
        if self.lives <= 0:
            return False
        else:
            self.status = self.Status.ALIVE
            self.explode_time = 0
            self.x = WIN_WIDTH / 2
            self.y = WIN_HEIGHT / 2
            self.angle = self.VIEW_ANGLE
            return True

    def move(self, dt):
        if self.status == self.Status.ALIVE:
            friction = 0.7

            self.rotation = 2 * pi * dt

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_KP4]:
                self.angle += self.rotation
            if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_KP6]:
                self.angle -= self.rotation

            if self.thrusting:
                self.thrust_x += self.thrust_speed * cos(self.angle) * dt
                self.thrust_y -= self.thrust_speed * sin(self.angle) * dt
            elif self.thrust_x != 0 or self.thrust_y != 0:
                self.thrust_x -= friction * self.thrust_x * dt
                self.thrust_y -= friction * self.thrust_y * dt

            self.x = wrap_x(self.x + self.thrust_x, self.radius)
            self.y = wrap_y(self.y + self.thrust_y, self.radius)
        elif self.status == self.Status.EXPLODING:
            self.explode_time += dt

            if self.explode_time > self.EXPLODE_DUR:
                if not self.respawn():
                    return False
        
        toRemove = []
        for laser in self.lasers:
            if not laser.move(dt):
                toRemove.append(laser)
            elif laser.travel_time > self.LASER_TIMER:
                toRemove.append(laser)
            elif laser.status == laser.Status.DESTROYED:
                toRemove.append(laser)
        for laser in toRemove:
            self.lasers.remove(laser)

        return True
    
    def explode(self):
        self.status = self.Status.EXPLODING
        self.thrust_x = 0
        self.thrust_y = 0
