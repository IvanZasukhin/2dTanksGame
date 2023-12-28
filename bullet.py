import pygame

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, *groups):
        super().__init__(*groups)
        self.pos = self.x, self.y = pos
        self.radius = 10
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, BLACK,
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
        direction.normalize_ip()
        self.vx = direction.x * 2
        self.vy = direction.y * 2

    def update(self, dt):
        self.rect = self.rect.move(self.vx, self.vy)
    #     if pygame.sprite.spritecollideany(self, horizontal_borders):
    #         self.vy = -self.vy
    #     if pygame.sprite.spritecollideany(self, vertical_borders):
    #         self.vx = -self.vx
