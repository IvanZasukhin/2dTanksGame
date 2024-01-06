import pygame

from settings import *
from timer import Timer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, level, pos, direction, player_owned, player_sprites, walls, *groups):
        super().__init__(*groups)
        self.level = level
        self.round = level.round
        self.walls = walls
        self.player_sprites = player_sprites
        self.direction = direction
        self.player_owned = player_owned
        self.radius = 9
        self.speed = self.player_owned.speed * 1.5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK,
                           (self.radius, self.radius), self.radius)
        direction.scale_to_length(38 + self.radius)
        self.pos = pygame.Vector2(pos[0] + direction.x, pos[1] + direction.y)
        self.rect = self.image.get_rect(center=self.pos)

        self.timers = {
            "time life": Timer(10000)
        }
        self.timers["time life"].activate()
        if pygame.sprite.spritecollideany(self, self.walls):
            self.kill()
            player_owned.kill()
            self.level.timers["wait round"].activate()

    def update(self, dt):
        self.update_timers()
        self.check_life_bullet()
        self.check_collision(dt)
        self.move(dt)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def check_life_bullet(self):
        if not self.timers["time life"].active or self.round != self.level.round:
            self.kill()

    def check_collision(self, dt):
        for sprite in self.walls.sprites():
            if sprite.is_collided_with(self):
                if self.direction:
                    self.direction.reflect_ip(sprite.direction)
                self.move(dt)
                if sprite.is_collided_with(self):
                    self.direction.reflect_ip(sprite.direction.rotate(90))
                    self.move(dt)
        for sprite in self.player_sprites.sprites():
            if sprite.is_collided_with(self):
                if sprite in self.player_sprites:
                    self.kill()
                    sprite.kill()
                    self.level.timers["wait round"].activate()

    def move(self, dt):
        try:
            self.direction.normalize_ip()
        except ValueError:
            pass
        self.pos += self.direction * dt * self.speed
        self.rect.center = self.pos
