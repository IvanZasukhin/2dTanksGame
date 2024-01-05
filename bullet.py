import pygame

from settings import *
from timer import Timer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, level, pos, direction, player_owned, player_sprites, collision_sprites, *groups):
        super().__init__(*groups)
        self.level = level
        self.collision_sprites = collision_sprites
        self.player_sprites = player_sprites
        self.direction = direction
        self.player_owned = player_owned
        self.radius = 9
        self.speed = self.player_owned.speed * 1.5
        self.lifetime = 10000
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK,
                           (self.radius, self.radius), self.radius)
        direction.scale_to_length(32 + self.radius + self.speed / 50)
        self.pos = pygame.Vector2(pos[0] + direction.x, pos[1] + direction.y)
        self.rect = self.image.get_rect(center=self.pos)

        self.timers = {
            "time life": Timer(self.lifetime)
        }
        self.timers["time life"].activate()

    def update(self, dt):
        self.update_timers()
        self.check_life_bullet()
        self.check_collision()
        self.move(dt)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def check_life_bullet(self):
        if not self.timers["time life"].active:
            self.kill()

    def check_collision(self):
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                if sprite in self.player_sprites:
                    self.timers["time life"].deactivate()
                    if sprite == self.player_sprites.sprites()[0]:
                        self.level.change_score(2)
                        self.player_sprites.sprites()[1].kill()
                    else:
                        self.level.change_score(1)
                        self.player_sprites.sprites()[0].kill()
                    sprite.kill()
                    self.level.generation()
                    self.level.setup()
                if self.direction.y == sprite.direction.y == 0 or self.direction.x == sprite.direction.x == 0:
                    self.direction = -sprite.direction
                else:
                    self.direction.reflect_ip(sprite.direction)
                break

    def move(self, dt):
        self.direction = self.direction.normalize()
        self.pos += self.direction * dt * self.speed
        self.rect.center = self.pos
