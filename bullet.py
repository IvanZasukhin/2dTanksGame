import pygame

from settings import *
from timer import Timer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, player_sprites, collision_sprites, *groups):
        super().__init__(*groups)
        self.collision_sprites = collision_sprites
        self.player_sprites = player_sprites
        self.direction = direction
        self.radius = 10
        self.speed = 300
        self.lifetime = 10000
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK,
                           (self.radius, self.radius), self.radius)
        direction.scale_to_length(40 + self.radius)
        self.pos = pygame.Vector2(pos[0] + direction.x, pos[1] + direction.y)
        self.rect = self.image.get_rect(center=self.pos)

        self.timers = {
            "time life": Timer(self.lifetime)
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
            self.timers["time life"].deactivate()

    def move(self, dt):
        self.direction = self.direction.normalize()
        self.pos += self.direction * dt * self.speed
        self.rect.center = self.pos
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                if self.direction.y == sprite.direction.y == 0 or self.direction.x == sprite.direction.x == 0:
                    self.direction = -sprite.direction
                else:
                    global e
                    print(e, sprite.direction)
                    e += 1
                    self.direction.reflect_ip(sprite.direction)
                break

e = 0
