from support import *
from timer import Timer
from settings import *

MANAGEMENT = {
    1: {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP,
        "down": pygame.K_DOWN, "attack": pygame.K_SPACE},
    2: {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w,
        "down": pygame.K_s, "attack": pygame.K_e}}


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, player_number, group, collision_sprites):
        super().__init__(group, collision_sprites)
        self.collision_sprites = collision_sprites
        self.player_sprites = group[1]

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
        self.rect = self.image.get_rect(center=pos)
        # Движение
        self.old_direction = 0
        self.direction_rotation = 0
        self.movement = 0
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2((0, -1))
        self.speed = 1
        self.speed_angle = 0.5
        # Таймер
        self.timers = {
            "attack": Timer(360)
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
            self.movement = -1
        elif keys[self.MANAGEMENT["down"]]:
            self.movement = 1
        if keys[self.MANAGEMENT["left"]]:
            self.direction_rotation = -1
        elif keys[self.MANAGEMENT["right"]]:
            self.direction_rotation = 1
        # атака
        if keys[self.MANAGEMENT["attack"]]:
            print("attack")

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animation(dt)

    def move(self, dt):
        self.status = "stop"
        # Движение
        movement_v = self.direction * self.movement
        if movement_v.length() > 0:
            self.speed_animation = 15
            self.status = "forward"
            movement_v.normalize_ip()
            self.pos += movement_v * dt * 100 * self.speed
            self.collision(dt, movement_v)

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
        self.image = pygame.transform.rotate(self.animations[self.status][int(self.frame)], angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.collision_turn(dt)

    def collision(self, dt, movement_v):
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                sprite.movement_collision(dt, movement_v)
                if self.movement:
                    self.pos += movement_v * dt * 100 * self.speed * self.movement

    def collision_turn(self, dt):
        for sprite in self.collision_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                if sprite in self.player_sprites:
                    sprite.movement_collision(dt, -self.direction)
                else:
                    self.movement_collision(dt, -self.direction)  # при столкновении со стенкой
                if self.old_direction != self.direction:
                    self.direction = self.direction.rotate(dt * 360 * self.speed_angle * -self.direction_rotation)
                    angle = self.direction.angle_to((0, -1))
                    self.image = pygame.transform.rotate(self.animations[self.status][int(self.frame)], angle)
                    self.rect = self.image.get_rect(center=self.pos)

    def movement_collision(self, dt, movement_v):
        self.pos += movement_v * dt * 100 * self.speed

    def is_collided_with(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)
