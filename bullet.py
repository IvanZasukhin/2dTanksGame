import pygame

from settings import *
from timer import Timer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, player_sprites, collision_sprites, *groups):
        super().__init__(*groups)
        self.collision_sprites = collision_sprites
        self.player_sprites = player_sprites
        self.pos = self.x, self.y = pygame.Vector2(pos[0], pos[1])
        self.radius = 10
        self.speed = 300
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, BLACK,
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
        self.direction = direction
        self.timers = {
            "time life": Timer(10000)
        }
        self.timers["time life"].activate()

    def update(self, dt):
        self.update_timers()
        self.check_life_bullet()
        # self.check_collision()
        self.move(dt)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def check_life_bullet(self):
        if not self.timers["time life"].active:
            self.kill()

    def check_collision(self):
        if pygame.sprite.spritecollide(self, self.player_sprites, True):
            self.kill()

    def move(self, dt):
        self.direction = self.direction.normalize()
        self.pos += self.direction * dt * self.speed
        self.rect.center = self.pos
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                block_hit = sprite # проверка
                if block_hit:
                    bl = block_hit[0].rect.left - self.rect.width / 4
                    br = block_hit[0].rect.right + self.rect.width / 4
                    nv = (0, 1) if bl < self.rect.centerx < br else (1, 0)
                    self.reflect(nv)

    def reflect(self, nv):
        self.direction = self.direction.reflect(pygame.math.Vector2(nv))
