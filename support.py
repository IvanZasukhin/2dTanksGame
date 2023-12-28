import os
import sys

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def import_image(path):
    surface_list = []
    for _, _, image_files in os.walk(path):
        for image in image_files:
            fullname = path + "/" + image
            im = pygame.image.load(fullname).convert_alpha()
            image_surface = pygame.transform.scale(im, (64, 64))
            surface_list.append(image_surface)
    return surface_list
