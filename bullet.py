from constants import *
from timer import Timer
import pygame.sprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, level, time_life, pos, radius, direction, speed, player_owned, player_sprites, walls,
                 all_sprites, bullet_sprites):
        super().__init__(all_sprites, bullet_sprites)
        self.level = level
        self.bullet_sprites = bullet_sprites
        self.round = level.round
        self.walls = walls
        self.player_sprites = player_sprites
        self.direction = direction
        self.player_owned = player_owned
        self.speed = speed * BULLET_SPEED_COF
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK,
                           (radius, radius), radius)
        direction.scale_to_length(38 + radius)
        self.pos = pygame.Vector2(pos[0] + direction.x, pos[1] + direction.y)
        self.rect = self.image.get_rect(center=self.pos)
        self.timers = {
            "time life": Timer(time_life)
        }
        self.timers["time life"].activate()
        if pygame.sprite.spritecollideany(self, self.walls):
            self.start_new_round(player_owned)

    def update(self, dt):
        self.update_timers()
        self.check_life_bullet()
        self.move(dt, self.direction)
        self.check_collision(dt)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def check_life_bullet(self):
        if not self.timers["time life"].active or self.round != self.level.round:
            self.kill()

    # noinspection PyTypeChecker
    def check_collision(self, dt):
        sprites = pygame.sprite.spritecollide(self, self.walls, False, pygame.sprite.collide_mask)
        if sprites:
            if self.direction:
                self.direction.reflect_ip(sprites[0].direction)
            self.move(dt, self.direction)
            if sprites[0].is_collided_with(self):
                self.direction = self.direction.rotate(180)
                self.move(dt, self.direction)
            while sprites[0].is_collided_with(self):
                self.move(dt, self.direction)
        sprites = pygame.sprite.spritecollide(self, self.player_sprites, False, pygame.sprite.collide_mask)
        if sprites:
            self.start_new_round(sprites[0])

    def start_new_round(self, sprite):
        self.kill()
        sprite.kill()
        self.level.timers["wait round"].activate()

    def move(self, dt, direction):
        self.pause()
        if direction:
            direction.normalize_ip()
        self.pos += direction * dt * self.speed
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def pause(self):
        self.timers["time life"].pause()
