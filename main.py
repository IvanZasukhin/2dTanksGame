import sys
import pygame
import pygame_menu

from level import Level
from settings import *


class Menu:
    def __init__(self):
        self.graphics_quality = 0
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Menu')
        self.menu = pygame_menu.Menu('Танки 2D', 400, 300,
                                     theme=pygame_menu.themes.THEME_DEFAULT)
        self.menu.add.button('Играть', self.start_the_game)
        self.menu.add.button('Настройки', self.settings_init)
        self.menu.add.button('Выйти', pygame_menu.events.EXIT)

        self.settings = pygame_menu.Menu('Настройки', 400, 300,
                                         theme=pygame_menu.themes.THEME_DEFAULT)
        self.settings.add.selector('Графика:', [('Низкая', 0), ('Средняя', 1), ('Высокая', 2)],
                                   onchange=self.set_graphics_quality, default=2)
        self.settings.add.selector('FPS:', [('30', 30), ('60', 60), ('120', 120)],
                                   onchange=self.set_fps, default=1)
        self.settings.add.button('Назад', self.menu_init)

        self.menu_init()

    def settings_init(self):
        self.settings.mainloop(self.screen)

    def menu_init(self):
        self.menu.mainloop(self.screen)

    def set_graphics_quality(self, *quality):
        self.graphics_quality = quality[1]

    def set_fps(self, *fps):
        self.fps = fps[1]

    def start_the_game(self):
        pygame.display.quit()
        settings = (self.graphics_quality, self.fps)
        game = Game(settings)
        game.run()


class Game:
    def __init__(self, settings):
        self.fps = settings[1]

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Танки 2')
        self.clock = pygame.time.Clock()
        self.level = Level(settings)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(self.fps) / 1000
            self.level.run(dt)
            pygame.display.update()
            pygame.display.set_caption("FPS: " + str(int(self.clock.get_fps())))  # FPS


if __name__ == '__main__':
    menu = Menu()
