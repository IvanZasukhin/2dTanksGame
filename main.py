import sys
import pygame
import pygame_menu

from level import Level
from settings import *


class Menu:
    def __init__(self):
        self.graphics_quality = 2
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Танки 2D')
        self.menu = pygame_menu.Menu('Танки 2D', 400, 300,
                                     theme=MY_THEME, mouse_enabled=False)
        self.menu.add.button('Играть', self.start_the_game)
        self.menu.add.button('Настройки', self.settings_init)
        self.menu.add.button('Выйти', pygame_menu.events.EXIT)

        self.menu.mainloop(self.screen)

    def settings_init(self):
        Settings(self.screen, self)

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
        self.graphics_quality = 2
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.stop = False

        if not screen:
            self.screen = pygame.display.set_mode(SCREEN_SIZE)
            self.graphics_quality = level.settings[0]
            self.fps = level.settings[1]

        self.background_image = pygame_menu.BaseImage(image_path="data/background.jpg")

        self.settings = pygame_menu.Menu('Настройки', 400, 300,
                                         theme=MY_THEME, mouse_enabled=False)
        self.settings.add.selector('Графика:', [('Низкая', 0), ('Средняя', 1), ('Высокая', 2)],
                                   onchange=self.set_graphics_quality, default=self.graphics_quality)
        self.settings.add.selector('FPS:', [('30', 30), ('60', 60), ('120', 120)],
                                   onchange=self.set_fps, default=self.fps // 60)
        self.settings.add.button('Назад', self.back)

        self.run()

    def back(self):
        if self.main_menu:
            self.stop = True
            self.settings.disable()
        else:
            self.level.change_settings(self.graphics_quality, self.fps)
            self.game.fps = self.fps
            self.stop = True
            self.settings.disable()

    def set_graphics_quality(self, *quality):
        if self.main_menu:
            self.main_menu.graphics_quality = quality[1]
        else:
            self.graphics_quality = quality[1]

    def set_fps(self, *fps):
        if self.main_menu:
            self.main_menu.fps = fps[1]
        else:
            self.fps = fps[1]

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
        self.level = Level(settings)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.image.save(self.screen, "data/background.jpg")
                        Settings(level=self.level, game=self)
            dt = self.clock.tick(self.fps) / 1000
            self.level.run(dt)
            pygame.display.update()
            pygame.display.set_caption("FPS: " + str(int(self.clock.get_fps())))  # FPS


if __name__ == '__main__':
    menu = Menu()
