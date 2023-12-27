import math
import pygame

from support import load_image


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # Генерация изображения
        self.image = pygame.transform.scale(load_image('tank.png'), (64, 64))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 5
        # Движение
        self.direction = pygame.math.Vector2()
        self.direction_angle = pygame.math.Vector2(1, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction_angle = self.direction_angle.rotate(self.angle)
        elif keys[pygame.K_RIGHT]:
            self.direction_angle = self.direction_angle.rotate(-self.angle)

        if keys[pygame.K_UP]:
            self.direction.y = self.direction_angle.y
            self.direction.x = self.direction_angle.x
        elif keys[pygame.K_DOWN]:
            self.direction.y = -self.direction_angle.y
            self.direction.x = -self.direction_angle.x
        else:
            self.direction.y = 0
            self.direction.x = 0

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = self.pos.y

    def update(self, dt):
        self.input()
        self.rotate()
        self.move(dt)

    def rotate(self):
        angle = pygame.math.Vector2.angle_to(self.direction_angle, pygame.math.Vector2(0, 1))
        self.image = pygame.transform.rotozoom(self.orig_image, angle, True)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos.x, self.pos.y = self.rect.x, self.rect.y
