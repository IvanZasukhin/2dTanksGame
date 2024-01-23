import pygame.sprite
from timer import Timer
from constants import *
from bullet import Bullet
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, level, settings, pos, vec, player_number, walls, boost_sprites, all_sprites, player_sprites):
        super().__init__(all_sprites, player_sprites)
        self.level = level
        self.graphics_quality = settings[0]
        self.all_sprites = all_sprites
        self.player_sprites = player_sprites
        self.boost_sprites = boost_sprites
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
        self.max_speed = PLAYER_MAX_SPEED
        self.speed = 0
        self.speed_angle = 0.5
        # настройки изображения
        self.image = self.animations[self.status][self.frame]
        self.orig_image = self.animations[self.status][0]
        angle = self.direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.image, angle)
        self.orig_image = pygame.transform.rotate(self.orig_image, angle)
        self.zoom()
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.orig_image)

        # Таймер
        self.timers = {
            "use attack": Timer(250)
        }
        # настройки пуль
        self.radius_bullet = RADIUS_BULLET
        self.speed_bullet = self.max_speed
        self.maximum_bullets = 10
        self.time_life_bullet = TIME_LIFE_BULLET

    def import_animation(self):
        for animation in self.animations.keys():
            full_path = f"data/animations/{self.player_number}/standard/{animation}"
            self.animations[animation] = self.import_image(full_path)

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
        if len(self.bullet_sprites) != self.maximum_bullets:
            Bullet(self.level, self.time_life_bullet, (self.pos.x, self.pos.y), self.radius_bullet, -self.direction,
                   self.speed_bullet, self, self.player_sprites, self.walls, self.all_sprites, self.bullet_sprites)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        if self.level.overlay.check_animation():
            self.input()
        self.move(dt)
        self.animation(dt)
        self.collision(dt)
        self.collision_turn(dt)
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
        self.rotate(angle)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.animations[self.status][int(self.frame)], angle)
        self.orig_image = pygame.transform.rotate(self.animations[self.status][0], angle)
        self.zoom()
        self.mask = pygame.mask.from_surface(self.orig_image)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    def zoom(self):
        if self.graphics_quality == 1:
            self.image = pygame.transform.scale_by(self.image, PLAYER_SCALE)
            self.orig_image = pygame.transform.scale_by(self.orig_image, PLAYER_SCALE)
        elif self.graphics_quality == 2:
            self.image = pygame.transform.smoothscale_by(self.image, PLAYER_SCALE)
            self.orig_image = pygame.transform.scale_by(self.orig_image, PLAYER_SCALE)

    # noinspection PyTypeChecker
    def collision(self, dt):
        if pygame.sprite.spritecollide(self, self.walls, False, pygame.sprite.collide_mask):
            movement_v = -self.direction * self.speed
            self.movement(dt, -movement_v)
        sprites = pygame.sprite.spritecollide(self, self.player_sprites, False, pygame.sprite.collide_mask)
        if len(sprites) != 1:
            movement_v = -self.direction * self.speed
            self.movement(dt, -movement_v)
        sprites = pygame.sprite.spritecollide(self, self.boost_sprites, False, pygame.sprite.collide_mask)
        if sprites:
            if self.check_boost(sprites[0].effect):
                sprites[0].kill()

    # noinspection PyTypeChecker
    def collision_turn(self, dt):
        if self.old_direction != self.direction:
            if pygame.sprite.spritecollide(self, self.walls, False, pygame.sprite.collide_mask):
                self.direction = self.direction.rotate(dt * 360 * self.speed_angle * -self.direction_rotation)
                angle = self.direction.angle_to((0, -1))
                self.rotate(angle)
            sprites = pygame.sprite.spritecollide(self, self.player_sprites, False, pygame.sprite.collide_mask)
            if len(sprites) != 1:
                self.direction = self.direction.rotate(dt * 360 * self.speed_angle * -self.direction_rotation)
                angle = self.direction.angle_to((0, -1))
                self.rotate(angle)

    def movement(self, dt, movement_v):
        self.pos += movement_v * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def get_boost(self, name_boost):
        if name_boost == "speed boost":
            self.max_speed *= 1.5
            self.speed_angle *= 1.2
            self.speed_bullet = self.max_speed
        elif name_boost == "attack boost":
            self.radius_bullet /= 1.5
            self.time_life_bullet /= 4
            self.timers["use attack"].duration /= 2
            self.speed_bullet *= 1.25
            self.maximum_bullets *= 2
            self.radius_bullet /= 2
            self.time_life_bullet /= 4
            self.timers["use attack"] = Timer(self.timers["use attack"].duration / 4)
            self.speed_bullet *= 1.25
            self.maximum_bullets *= 2
        self.timers[name_boost] = Timer(5000, lambda: self.stop_boost(name_boost))
        self.timers[name_boost].activate()

    def stop_boost(self, name_boost):
        self.timers[name_boost].activate()
        self.timers[name_boost].freeze = True
        if name_boost == "speed boost":
            self.max_speed = self.max_speed / 2
            self.speed_angle /= 1.2
            self.speed_bullet = self.max_speed
        if name_boost == "attack boost":
            self.radius_bullet *= 2
            self.time_life_bullet *= 4
            self.timers["use attack"] = Timer(self.timers["use attack"].duration * 4)
            self.speed_bullet /= 1.25
            self.maximum_bullets /= 2

    def check_boost(self, effect):
        try:
            if self.timers[effect].active:
                return False
        except KeyError:
            pass
        self.get_boost(effect)
        return True

    def import_image(self, path):
        surface_list = []
        for _, _, image_files in walk(path):
            for im in image_files:
                fullname = path + "/" + im
                im = pygame.image.load(fullname).convert_alpha()
                image_surface = pygame.transform.scale(im, (512, 512))
                if self.graphics_quality == 0:
                    image_surface = pygame.transform.scale_by(image_surface, PLAYER_SCALE)
                surface_list.append(image_surface)
        return surface_list
