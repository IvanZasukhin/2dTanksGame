import pygame as pg
import os
import sys
import math

screen = pg.display.set_mode((800, 600))
all_sprites = pg.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tank(pg.sprite.Sprite):
    image = load_image('tank.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pg.transform.scale(Tank.image, (64, 64))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0

    def update(self, keys):
        if keys[pg.K_LEFT]:
            self.angle += 5
        if keys[pg.K_RIGHT]:
            self.angle -= 5
        if keys[pg.K_UP]:
            self.rect.x += 10 * math.sin(math.radians(self.angle))
            self.rect.y += 10 * math.cos(math.radians(self.angle))
        if keys[pg.K_DOWN]:
            self.rect.x -= 10 * math.sin(math.radians(self.angle))
            self.rect.y -= 10 * math.cos(math.radians(self.angle))
        self.rotate()

    def rotate(self):
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pg.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)


def main():
    clock = pg.time.Clock()
    running = True
    Tank((400, 300))
    while running:
        screen.fill('black')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        all_sprites.update(keys)
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
