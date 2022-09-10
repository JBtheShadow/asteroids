import pygame
import json
from pathlib import Path
from math import cos, sin, sqrt
from random import random

from globals import *


def get_distance(x1, y1, x2 = None, y2 = None):
    if x2 and y2:
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    else:
        return sqrt(x1 ** 2 + y1 ** 2)

def get_x(point_or_rect):
    return point_or_rect[0]

def get_y(point_or_rect):
    return point_or_rect[1]

def get_size(rect):
    return get_width(rect), get_height(rect)

def get_width(rect):
    return rect[2]

def get_height(rect):
    return rect[3]

def does_circle_overlap_rect(center, radius, rect):
    if get_x(center) + radius >= get_x(rect) and get_x(center) - radius <= get_x(rect) + get_width(rect):
        if get_y(center) + radius >= get_y(rect) and get_y(center) - radius <= get_y(rect) + get_height(rect):
            return True
    return False

def do_circles_overlap(center1, radius1, center2, radius2):
    return get_distance(get_x(center1), get_y(center1), get_x(center2), get_y(center2)) <= radius1 + radius2

def rand_sign():
    return 1 if random() < 0.5 else -1

def get_rect(points):
    min_x = min(map(get_x, points))
    max_x = max(map(get_x, points))
    min_y = min(map(get_y, points))
    max_y = max(map(get_y, points))
    return min_x, min_y, max_x - min_x, max_y - min_y

def move_points(points, x_offset, y_offset):
    return list(map(lambda point: (get_x(point) + x_offset, get_y(point) + y_offset), points))

def wrap_x(x, radius = 0):
    if x + radius < 0:
        return WIN_WIDTH + radius
    elif x - radius > WIN_WIDTH:
        return -radius
    else:
        return x

def wrap_y(y, radius = 0):
    if y + radius < 0:
        return WIN_HEIGHT + radius
    elif y - radius > WIN_HEIGHT:
        return -radius
    else:
        return y

def draw_polygon(win: pygame.Surface, color, points, width):
    pygame.draw.polygon(win, color, points, width)

def draw_hitbox(win: pygame.Surface, color, center, radius, width):
    pygame.draw.circle(win, color, center, 1)
    pygame.draw.circle(win, color, center, radius, width)

def draw_explosion(win: pygame.Surface, big_color, small_color, center, big_radius, small_radius):
    pygame.draw.circle(win, big_color, center, big_radius)
    pygame.draw.circle(win, small_color, center, small_radius)

def draw_big_explosion(win: pygame.Surface, big_color, medium_color, small_color, center, big_radius, medium_radius, small_radius):
    pygame.draw.circle(win, big_color, center, big_radius)
    pygame.draw.circle(win, medium_color, center, medium_radius)
    pygame.draw.circle(win, small_color, center, small_radius)

def draw_ship_shape(win: pygame.Surface, x, y, radius, angle, color, width, debugging):
    si, co = sin(angle), cos(angle)
    points = [
        (x + 4/3 * co * radius,        y - 4/3 * si * radius),
        (x - (2/3 * co + si) * radius, y + (2/3 * si - co) * radius),
        (x - 1/2 * co * radius,        y + 1/2 * si * radius),
        (x - (2/3 * co - si) * radius, y + (2/3 * si + co) * radius)
    ]
    draw_polygon(win, color, points, width)

def create_path_if_not_exists(file_path):
    path = Path(file_path)
    path.parent.mkdir(parents= True, exist_ok= True)

def create_json_if_not_exists(file_path):
    path = Path(file_path)
    if not path.exists():
        file = open(file_path, "w")
        file.write(json.dumps({"highScore": 0}))
        file.close()

def read_json(file_name):
    full_file_path = f"./data/{file_name}.json"
    
    create_path_if_not_exists(full_file_path)
    create_json_if_not_exists(full_file_path)
    
    file = open(full_file_path, "r")
    data = file.read()
    file.close()

    return json.loads(data)

def write_json(file_name, data):
    full_file_path = f"./data/{file_name}.json"

    create_path_if_not_exists(full_file_path)

    file = open(full_file_path, "w")
    file.write(json.dumps(data))
    file.close()