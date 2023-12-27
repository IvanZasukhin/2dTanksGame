import pygame

from support import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, player_number=1):
        super().__init__(group)
        # Генерация изображения
        self.image = pygame.transform.scale(load_image('tank.png'), (64, 64))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        # Движение
        self.direction = pygame.math.Vector2()
        self.direction_angle = pygame.math.Vector2(1, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100
        self.angle = 3
        # Управление
        self.MANAGEMENT = {
            1: {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP,
                "down": pygame.K_DOWN, "attack": pygame.K_SPACE},
            2: {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w,
                "down": pygame.K_s, "attack": pygame.K_e}}[player_number]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[self.MANAGEMENT["left"]]:
            self.direction_angle = self.direction_angle.rotate(-self.angle)
        elif keys[self.MANAGEMENT["right"]]:
            self.direction_angle = self.direction_angle.rotate(self.angle)

        if keys[self.MANAGEMENT["up"]]:
            self.direction.y = self.direction_angle.y
            self.direction.x = self.direction_angle.x
        elif keys[self.MANAGEMENT["down"]]:
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
        self.move(dt)
        self.rotate()

    def rotate(self):
        angle = pygame.math.Vector2.angle_to(self.direction_angle, pygame.math.Vector2(0, 1))
        self.image = pygame.transform.rotozoom(self.orig_image, angle, 0.5)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
