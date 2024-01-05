import os
from pygame import image, transform
from settings import *


def import_image(path):
    surface_list = []
    for _, _, image_files in os.walk(path):
        for im in image_files:
            fullname = path + "/" + im
            im = image.load(fullname).convert_alpha()
            image_surface = transform.scale(im, (512, 512))
            if GRAPHICS_QUALITY != 1:
                image_surface = transform.smoothscale_by(image_surface, PLAYER_ZOOM)
            surface_list.append(image_surface)
    return surface_list


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
