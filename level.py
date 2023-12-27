import pygame

from settings import *
from player import Tank


class Level:
    def __init__(self):
        # спрайт окна
        self.display_surface = pygame.display.get_surface()
        # спрайты
        self.all_sprites = pygame.sprite.Group()
        Tank((400, 300), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill(BLACK)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)