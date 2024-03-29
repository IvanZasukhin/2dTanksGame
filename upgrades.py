from constants import *
import pygame.sprite


class Boost(pygame.sprite.Sprite):
    def __init__(self, pos, player_sprites, all_sprites, boost_sprites, color=PURPLE):
        super().__init__(all_sprites, boost_sprites)
        self.player_sprites = player_sprites
        self.all_sprites = all_sprites
        self.boost_sprites = boost_sprites
        self.graphics_quality = 2
        self.effect = "NONE effect"
        self.color = color

        size = (32, 32)
        rect_size = 32

        self.scale = 1
        deviation = 0.1
        self.scale_max = self.scale + deviation
        self.scale_min = self.scale - deviation
        self.angle = 0
        self.ratio_animation = -800
        self.speed_animation = 100

        self.original_image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, self.color, (0, 0, rect_size,
                                                           rect_size))
        self.image = self.original_image

        self.pos = pygame.Vector2(pos[0], pos[1])
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box = self.rect.copy()

        self.mask = pygame.mask.from_surface(self.image)

        self.zoom()

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hit_box.center)
        self.mask = pygame.mask.from_surface(self.image)

    def zoom(self):
        if self.graphics_quality == 2:
            self.image = pygame.transform.smoothscale_by(self.image, self.scale)
        else:
            self.image = pygame.transform.scale_by(self.image, self.scale)
        self.rect = self.image.get_rect(center=self.hit_box.center)


class SpeedBoost(Boost):
    def __init__(self, pos, player_sprites, all_sprites, boost_sprites):
        super().__init__(pos, player_sprites, all_sprites, boost_sprites, color=GREEN)
        self.effect = "speed boost"


class AttackBoost(Boost):
    def __init__(self, pos, player_sprites, all_sprites, boost_sprites):
        super().__init__(pos, player_sprites, all_sprites, boost_sprites, color=RED)
        self.effect = "attack boost"
