import pygame

from settings import *
from timer import Timer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, player_sprites, v_walls, h_walls, *groups):
        super().__init__(*groups)
        self.v_walls = v_walls
        self.h_walls = h_walls
        self.player_sprites = player_sprites
        self.pos = self.x, self.y = pos[0] + direction.x * 65, pos[1] + direction.y * 65
        self.radius = 10
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, BLACK,
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
        direction.normalize_ip()
        self.speed = 5
        self.vx = direction.x * 2 * self.speed
        self.vy = direction.y * 2 * self.speed
        self.timer = Timer(5000)
        self.timer.activate()

    def update(self, dt):
        self.update_timers()
        if pygame.sprite.spritecollide(self, self.player_sprites, True):
            self.kill()
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollide(self, self.h_walls, False):
            self.vy = -self.vy
        if pygame.sprite.spritecollide(self, self.v_walls, False):
            self.vx = -self.vx

    def update_timers(self):
        self.timer.update()
        if not self.timer.active:
            self.kill()

    def is_collided_with(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)
