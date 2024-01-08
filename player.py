import pygame.sprite

from support import *
from timer import Timer
from constants import *
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, level, settings, pos, vec, player_number, all_sprites, player_sprites, walls):
        super().__init__(all_sprites, player_sprites)
        self.level = level
        self.graphics_quality = settings[0]
        self.all_sprites = all_sprites
        self.player_sprites = player_sprites
        self.walls = walls
        self.bullet_sprites = pygame.sprite.Group()
        self.player_number = player_number
        self.MANAGEMENT = MANAGEMENT[self.player_number]
        self.bullet_group = []
        # Генерация изображения
        # настройки анимации
        self.animations = {"stop": [], "forward": [], "left": [], "right": [], "back": []}
        self.status = "stop"
        self.speed_animation = 15
        self.frame = 0
        self.import_animation()
        # Движение
        self.old_direction = 0
        self.direction_rotation = 0
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2(vec)
        if self.direction:
            self.direction.normalize_ip()
        self.max_speed = 200
        self.speed = 0
        self.speed_angle = 0.5
        # настройки изображения
        self.player_zoom = PLAYER_ZOOM
        self.image = self.animations[self.status][self.frame]
        self.orig_image = self.animations[self.status][0]
        angle = self.direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.image, angle)
        self.orig_image = pygame.transform.rotate(self.orig_image, angle)
        if self.graphics_quality == 1:
            self.image = pygame.transform.scale_by(self.image, self.player_zoom)
            self.orig_image = pygame.transform.scale_by(self.orig_image, self.player_zoom)
        elif self.graphics_quality == 2:
            self.image = pygame.transform.smoothscale_by(self.image, self.player_zoom)
            self.orig_image = pygame.transform.scale_by(self.orig_image, self.player_zoom)
        self.rect = self.image.get_rect(center=pos)
        self.hit_box = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.orig_image)

        # Таймер
        self.timers = {
            "use attack": Timer(250)
        }

    def import_animation(self):
        for animation in self.animations.keys():
            full_path = f"data/animations/{self.player_number}/standard/{animation}"
            self.animations[animation] = import_image(full_path, self.graphics_quality)

    def input(self):
        keys = pygame.key.get_pressed()
        self.old_direction = self.direction.copy()
        self.speed = 0
        self.direction_rotation = 0
        if keys[self.MANAGEMENT["up"]]:
            self.speed = self.max_speed
        elif keys[self.MANAGEMENT["down"]]:
            self.speed = -self.max_speed
        if keys[self.MANAGEMENT["left"]]:
            self.direction_rotation = -1
        elif keys[self.MANAGEMENT["right"]]:
            self.direction_rotation = 1
        # атака
        if not self.timers["use attack"].active and keys[self.MANAGEMENT["attack"]]:
            self.use_attack()

    def use_attack(self):
        self.timers["use attack"].activate()
        maximum_bullets = 10
        if len(self.bullet_sprites) != maximum_bullets:
            Bullet(self.level, (self.pos.x, self.pos.y), -self.direction, self, self.player_sprites,
                   self.walls, self.all_sprites, self.bullet_sprites)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        if self.level.overlay.check_animation():
            self.input()
        self.move(dt)
        self.animation(dt)
        self.collision_turn(dt)
        self.collision(dt)
        self.update_timers()

    def move(self, dt):
        self.status = "stop"
        # поворот танка
        if self.direction_rotation < 0:
            self.status = "left"
            self.speed_animation = 30
        elif self.direction_rotation > 0:
            self.speed_animation = 30
            self.status = "right"
        self.direction = self.direction.rotate(dt * 360 * self.speed_angle * self.direction_rotation)
        # Движение
        movement_v = (-self.direction * self.speed)
        if movement_v.length() > 0:
            self.speed_animation = 15
            self.status = "forward"
            self.movement(dt, movement_v)

    def animation(self, dt):
        self.frame += self.speed_animation * dt
        if self.frame >= len(self.animations[self.status]):
            self.frame = 0
        self.image = self.animations[self.status][int(self.frame)]
        angle = self.direction.angle_to((0, -1))
        self.rotate_player(angle)

    def rotate_player(self, angle):
        self.image = pygame.transform.rotate(self.animations[self.status][int(self.frame)], angle)
        self.orig_image = pygame.transform.rotate(self.animations[self.status][0], angle)
        if self.graphics_quality == 1:
            self.image = pygame.transform.scale_by(self.image, self.player_zoom)
            self.orig_image = pygame.transform.scale_by(self.orig_image, self.player_zoom)
        elif self.graphics_quality == 2:
            self.image = pygame.transform.smoothscale_by(self.image, self.player_zoom)
            self.orig_image = pygame.transform.scale_by(self.orig_image, self.player_zoom)
        self.mask = pygame.mask.from_surface(self.orig_image)
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def collision(self, dt):
        for sprite in self.walls.sprites():
            if sprite.is_collided_with(self):
                movement_v = -self.direction
                self.movement(dt, -movement_v)
            if self is not sprite and sprite.is_collided_with(self):
                movement_v = -self.direction * self.speed
                self.movement(dt, -movement_v)

    def collision_turn(self, dt):
        for sprite in self.walls.sprites():
            if sprite.is_collided_with(self):
                if self.old_direction != self.direction:
                    self.direction = self.direction.rotate(dt * 360 * self.speed_angle * -self.direction_rotation)
                    angle = self.direction.angle_to((0, -1))
                    self.rotate_player(angle)
        for sprite in self.player_sprites.sprites():
            if self is not sprite and sprite.is_collided_with(self):
                if self.old_direction != self.direction:
                    self.direction = self.direction.rotate(dt * 360 * self.speed_angle * -self.direction_rotation)
                    angle = self.direction.angle_to((0, -1))
                    self.rotate_player(angle)

    def is_collided_with(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)

    def movement(self, dt, movement_v):
        self.pos += movement_v * dt
        self.hit_box.centerx = round(self.pos.x)
        self.hit_box.centery = round(self.pos.y)
        self.rect.center = self.hit_box.center
