import sys
import pygame
import pygame_menu

from level import Level1, Level2
from constants import *
from os import remove, path
from support import get_settings


class MainMenu:
    def __init__(self):
        self.settings_menu = None
        self.game_selection = None

        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Танки 2D')
        self.menu = pygame_menu.Menu('Танки 2D', 400, 300,
                                     theme=MY_THEME, mouse_enabled=False, mouse_visible=False)
        self.menu.add.button('Играть', self.start_the_game)

        self.menu.add.button('Настройки', self.settings_init)
        self.menu.add.button('Выйти', pygame_menu.events.EXIT)

        self.menu.mainloop(self.screen)

    def activate(self):
        self.menu.enable()
        self.menu.mainloop(self.screen)

    def settings_init(self):
        pygame.image.save(self.screen, "data/background.jpg")
        if self.settings_menu:
            self.settings_menu.activate()
        else:
            self.settings_menu = Settings(self.screen, self)

    def start_the_game(self):
        if self.game_selection:
            self.game_selection.activate()
        else:
            self.game_selection = GameSelection(self.screen)


class GameSelection:
    def __init__(self, screen):
        self.screen = screen
        self.max_round, self.selected_game = get_settings()[2:]

        self.menu = pygame_menu.Menu('Выбор уровня', 400, 300,
                                     theme=MY_THEME, mouse_enabled=False)
        self.menu.add.button('Играть', self.start_game)
        self.menu.add.selector('Раундов: ', [('3', 3), ('5', 5), ('10', 10), ('15', 15)], default=self.max_round // 5,
                               onchange=self.set_rounds_count)
        self.menu.add.selector('Уровень: ', [('Со стенами', 0), ('Без стен', 1)], default=self.selected_game,
                               onchange=self.set_selected_game)
        self.menu.add.button('Главное меню', self.back_to_main)

        self.menu.mainloop(self.screen)

    def activate(self):
        self.menu.enable()
        self.menu.mainloop(self.screen)

    def back_to_main(self):
        self.change_game_settings()
        self.menu.disable()

    def set_rounds_count(self, *max_round):
        self.max_round = max_round[1]

    def set_selected_game(self, *selected_game):
        self.selected_game = selected_game[1]

    def change_game_settings(self):
        settings = get_settings()[:2]
        with open('data/settings.txt', 'w') as file_settings:
            file_settings.write(f'{settings[0]}\n{settings[1]}\n{self.max_round}\n{self.selected_game}')

    def start_game(self):
        self.menu.disable()
        self.change_game_settings()
        pygame.display.quit()
        game = Game()
        game.run()


class FinalMenu:
    def __init__(self, blue_wins, red_wins):
        self.screen = pygame.display.set_mode((400, 300))
        self.menu = pygame_menu.Menu('Танки 2D', 400, 300,
                                     theme=MY_THEME, mouse_enabled=False, mouse_visible=False)
        if blue_wins > red_wins:
            self.menu.add.label('Синий победил', font_color=BLUE)
        elif blue_wins < red_wins:
            self.menu.add.label('Красный победил', font_color=RED)
        else:
            self.menu.add.label('Ничья', font_color=BLACK)

        self.menu.add.label(f'Счёт {blue_wins} : {red_wins}', font_color=BLACK)
        self.menu.add.button('Главное меню', self.back_to_main)
        self.menu.add.button('Выйти', pygame_menu.events.EXIT)

        self.menu.mainloop(self.screen)

    def back_to_main(self):
        pygame.display.quit()
        MainMenu()


class Settings:
    def __init__(self, screen=None, main_menu=None, level=None, game=None):
        self.screen = screen
        self.main_menu = main_menu
        self.level = level
        self.game = game
        self.graphics_quality, self.fps = get_settings()[:2]
        self.clock = pygame.time.Clock()
        # self.stop = False

        self.settings = pygame_menu.Menu('Настройки', 400, 300,
                                         theme=MY_THEME, mouse_enabled=False, mouse_visible=False)
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
        # self.stop = False
        self.settings.enable()
        self.run()

    def proceed(self):
        self.change_settings()
        self.level.settings[0], self.level.settings[1] = get_settings()[:2]
        get_settings()
        self.game.fps = self.fps
        # self.stop = True
        self.settings.disable()
        remove('data/background.jpg')

    def back_to_main(self):
        self.change_settings()
        if self.main_menu:
            # self.stop = True
            self.settings.disable()
        else:
            # self.stop = True
            self.settings.disable()
            pygame.display.quit()
            remove('data/background.jpg')
            MainMenu()
        remove('data/background.jpg')

    def set_graphics_quality(self, *quality):
        self.graphics_quality = quality[1]

    def set_fps(self, *fps):
        self.fps = fps[1]

    def change_settings(self):
        settings = get_settings()[2:]
        with open('data/settings.txt', 'w') as file_settings:
            file_settings.write(f'{self.graphics_quality}\n{self.fps}\n{settings[0]}\n{settings[1]}')

    def background(self):
        self.background_image.draw(self.screen)

    def run(self):
        self.settings.mainloop(self.screen, self.background)
        # while True:
        #     if self.stop:
        #         self.settings.disable()
        #         break
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_ESCAPE:
        #                 self.proceed()
        #     self.clock.tick(self.fps)
        #     self.settings.mainloop(self.screen, self.background)
        #     pygame.display.flip()


class Game:
    def __init__(self):
        self.settings = get_settings()
        self.fps = self.settings[1]
        changed_level = self.settings[3]

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Танки 2D')
        self.clock = pygame.time.Clock()
        self.settings_menu = None
        if changed_level == 0:
            self.level = Level1(self)
        elif changed_level == 1:
            self.level = Level2(self)

    def end_game(self, blue_wins, red_wins):
        FinalMenu(blue_wins, red_wins)

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
            pygame.mouse.set_visible(False)
            pygame.display.update()
            pygame.display.set_caption("FPS: " + str(int(self.clock.get_fps())))  # FPS


if __name__ == '__main__':
    pygame.init()
    with open('data/settings.txt', 'r+') as file:
        if not file.read().strip():
            file.write(f'2\n60\n5\n1')
    MainMenu()
    if path.exists('data/background.jpg'):
        remove('data/background.jpg')
