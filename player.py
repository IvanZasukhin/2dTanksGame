import pygame.sprite

from support import *
from timer import Timer
from settings import *
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, player_number, all_sprites, player_sprites, collision_sprites, bullet_sprites, walls):
        super().__init__(all_sprites, player_sprites, collision_sprites)
        self.all_sprites = all_sprites
        self.player_sprites = player_sprites
        self.walls = walls
        self.collision_sprites = collision_sprites
        self.bullet_sprites = bullet_sprites
        self.MANAGEMENT = MANAGEMENT[player_number]
        # Генерация изображения

        # настройки анимации
        self.animations = {"stop": [], "forward": [], "left": [], "right": [], "back": []}
        self.status = "stop"
        self.speed_animation = 15
        self.frame = 0
        self.import_animation()
        # настройки изображения
        self.image = self.animations[self.status][self.frame]
        self.orig_image = self.animations[self.status][self.frame]
        self.player_size = 0.125
        self.image = pygame.transform.rotozoom(self.image, 0, self.player_size)
        self.rect = self.image.get_rect(center=pos)
        self.hit_box = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)
        # Движение
        self.old_direction = 0
        self.movement = 0
        self.direction_rotation = 0
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2((0, 1))
        self.speed = 200
        self.speed_angle = 0.5
        # Таймер
        self.timers = {
            "use attack": Timer(500)
        }

    def import_animation(self):
        for animation in self.animations.keys():
            full_path = "data/animations/standard/" + animation
            self.animations[animation] = import_image(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        self.old_direction = self.direction.copy()
        self.movement = 0
        self.direction_rotation = 0
        if keys[self.MANAGEMENT["up"]]:
            self.movement = 1
        elif keys[self.MANAGEMENT["down"]]:
            self.movement = -1
        if keys[self.MANAGEMENT["left"]]:
            self.direction_rotation = -1
        elif keys[self.MANAGEMENT["right"]]:
            self.direction_rotation = 1
        # атака
        if not self.timers["use attack"].active and keys[self.MANAGEMENT["attack"]]:
            self.use_attack()

    def use_attack(self):
        self.timers["use attack"].activate()
        Bullet((self.pos.x, self.pos.y), -self.direction, self.player_sprites, self.collision_sprites,
               self.all_sprites,
               self.bullet_sprites)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animation(dt)
        self.update_timers()

    def move(self, dt):
        self.status = "stop"
        # Движение
        movement_v = -self.direction * self.movement
        if movement_v.length() > 0:
            self.speed_animation = 15
            self.status = "forward"
            movement_v.normalize_ip()
            self.pos += movement_v * dt * self.speed
            self.hit_box.centerx = round(self.pos.x)
            self.hit_box.centery = round(self.pos.y)
            self.rect.center = self.hit_box.center
        self.collision(dt)

        # поворот танка
        if self.direction_rotation < 0:
            self.status = "left"
            self.speed_animation = 30
        elif self.direction_rotation > 0:
            self.speed_animation = 30
            self.status = "right"
        self.direction = self.direction.rotate(dt * 360 * self.speed_angle * self.direction_rotation)

    def animation(self, dt):
        self.frame += self.speed_animation * dt
        if self.frame >= len(self.animations[self.status]):
            self.frame = 0
        self.image = self.animations[self.status][int(self.frame)]
        angle = self.direction.angle_to((0, -1))
        self.image = pygame.transform.rotozoom(self.animations[self.status][int(self.frame)], angle, self.player_size)
        self.rect = self.image.get_rect(center=self.hit_box.center)
        self.orig_image = pygame.transform.rotozoom(self.animations[self.status][0], angle, self.player_size)
        self.mask = pygame.mask.from_surface(self.orig_image)
        self.collision_turn(dt)

    def collision(self, dt):
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                movement_v = -self.direction * self.movement
                self.movement_collision(dt, movement_v)
                # print(self.direction.angle_to(sprite.direction) % 180)
                # self.direction_rotation = 0
                # if 90 < self.direction.angle_to(sprite.direction) < 180:
                #     self.direction_rotation = 1
                # elif 0 < self.direction.angle_to(sprite.direction) < 90:
                #     self.direction_rotation = 1
                # self.direction = self.direction.rotate(dt * 360 * (self.speed_angle / 2) * self.direction_rotation)

    def collision_turn(self, dt):
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                if self.old_direction != self.direction:
                    self.direction = self.direction.rotate(dt * 360 * self.speed_angle * -self.direction_rotation)
                    angle = self.direction.angle_to((0, -1))
                    self.image = pygame.transform.rotozoom(self.animations[self.status][int(self.frame)], angle,
                                                           self.player_size)

                    self.orig_image = pygame.transform.rotozoom(self.animations[self.status][0], angle,
                                                                self.player_size)
                    self.mask = pygame.mask.from_surface(self.orig_image)
                    self.rect = self.image.get_rect(center=self.hit_box.center)

    def is_collided_with(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)

    def movement_collision(self, dt, movement_v):
        self.pos -= movement_v * dt * self.speed
        self.hit_box.centerx = round(self.pos.x)
        self.hit_box.centery = round(self.pos.y)
        self.rect.center = self.hit_box.center


def is_collided_with(self, sprite):
    return pygame.sprite.collide_mask(self, sprite)
