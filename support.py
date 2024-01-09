from os import walk
from pygame import image, transform
from constants import *


def import_image(path, graphics_quality):
    surface_list = []
    for _, _, image_files in walk(path):
        for im in image_files:
            fullname = path + "/" + im
            im = image.load(fullname).convert_alpha()
            image_surface = transform.scale(im, (512, 512))
            if graphics_quality == 0:
                image_surface = transform.scale_by(image_surface, PLAYER_ZOOM)
            surface_list.append(image_surface)
    return surface_list


def get_settings():
    with open('data/settings.txt', 'r') as file:
        return [int(line.strip()) for line in file.readlines()]


def remove_walls(current, next_walls):
    dx = current.x - next_walls.x
    if dx == 1:
        current.walls['left'] = False
        next_walls.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next_walls.walls['left'] = False
    dy = current.y - next_walls.y
    if dy == 1:
        current.walls['top'] = False
        next_walls.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next_walls.walls['top'] = False
