import sys
import pygame
import pygame_menu

from level import Level
from constants import *
from os import remove, path
from support import get_settings


class Menu:
    def __init__(self):
        self.graphics_quality, self.fps = get_settings()
        self.settings_menu = None

        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Танки 2D')
        self.menu = pygame_menu.Menu('Танки 2D', 400, 300,
                                     theme=MY_THEME, mouse_enabled=False)
        self.menu.add.button('Играть', self.start_the_game)
        self.menu.add.button('Настройки', self.settings_init)
        self.menu.add.button('Выйти', pygame_menu.events.EXIT)

        self.menu.mainloop(self.screen)

    def settings_init(self):
        pygame.image.save(self.screen, "data/background.jpg")
        if self.settings_menu:
            self.settings_menu.activate()
        else:
            self.settings_menu = Settings(self.screen, self)

    def start_the_game(self):
        pygame.display.quit()
        settings = [self.graphics_quality, self.fps]
        game = Game(settings)
        game.run()


class Settings:
    def __init__(self, screen=None, main_menu=None, level=None, game=None):
        self.screen = screen
        self.main_menu = main_menu
        self.level = level
        self.game = game
        self.graphics_quality, self.fps = get_settings()
        self.clock = pygame.time.Clock()
        self.stop = False

        self.settings = pygame_menu.Menu('Настройки', 400, 300,
                                         theme=MY_THEME, mouse_enabled=False)
        self.background_image = pygame_menu.BaseImage(image_path="data/background.jpg")

        if game:
            self.screen = pygame.display.set_mode(SCREEN_SIZE)
            self.settings.add.button('Продолжить', self.proceed)

        self.settings.add.selector('Графика:', [('Низкая', 0), ('Средняя', 1), ('Высокая', 2)],
                                   onchange=self.set_graphics_quality, default=self.graphics_quality)
        self.settings.add.selector('FPS:', [('30', 30), ('60', 60), ('120', 120)],
                                   onchange=self.set_fps, default=self.fps // 60)
        self.settings.add.button('Главное меню', self.back_to_main)

        self.run()

    def activate(self):
        self.background_image = pygame_menu.BaseImage(image_path="data/background.jpg")
        self.settings.enable()
        self.run()

    def proceed(self):
        self.change_settings()
        get_settings()
        self.game.fps = self.fps
        self.stop = True
        self.settings.disable()
        remove('data/background.jpg')

    def back_to_main(self):
        self.change_settings()
        if self.main_menu:
            self.stop = True
            self.settings.disable()
        else:
            self.stop = True
            self.settings.disable()
            pygame.display.quit()
            remove('data/background.jpg')
            Menu()
        remove('data/background.jpg')

    def set_graphics_quality(self, *quality):
        self.graphics_quality = quality[1]

    def set_fps(self, *fps):
        self.fps = fps[1]

    def change_settings(self):
        with open('data/settings.txt', 'w') as file_settings:
            file_settings.write(f'{self.graphics_quality}\n{self.fps}')

    def background(self):
        self.background_image.draw(self.screen)

    def run(self):
        while True:
            self.clock.tick(self.fps)
            self.settings.mainloop(self.screen, self.background, fps_limit=self.fps)
            pygame.display.flip()

            if self.stop:
                self.settings.disable()
                break


class Game:
    def __init__(self, settings):
        self.fps = settings[1]

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Танки 2D')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.settings_menu = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.image.save(self.screen, "data/background.jpg")
                        if self.settings_menu:
                            self.settings_menu.activate()
                        else:
                            self.settings_menu = Settings(game=self, level=self.level)
                            self.level.settings_menu = self.settings_menu

            dt = self.clock.tick(self.fps) / 1000
            self.level.run(dt)
            pygame.display.update()
            pygame.display.set_caption("FPS: " + str(int(self.clock.get_fps())))  # FPS


if __name__ == '__main__':
    pygame.init()
    with open('data/settings.txt') as file:
        if not file.read():
            file.write(f'2\n60')
    Menu()
    if path.exists('data/background.jpg'):
        remove('data/background.jpg')
