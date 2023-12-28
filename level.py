import pygame

from settings import *
from player import Player


class Level:
    def __init__(self):
        # спрайт окна
        self.display_surface = pygame.display.get_surface()
        # спрайты
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        Player((300, 300), 1, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites)
        Player((400, 300), 2, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites)

    def run(self, dt):
        self.display_surface.fill(WHITE)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
