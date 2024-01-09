from map import *
from player import Player
from constants import *
from support import remove_walls
from overlay import Overlay
from random import randint, uniform
from timer import Timer
from support import get_settings


class Level:
    def __init__(self):
        self.settings = get_settings()
        # окно
        self.screen = pygame.display.get_surface()
        self.settings_menu = None
        # карта
        self.grid_cells = []
        self.stack = []
        self.tile = 175
        self.cols, self.rows = SCREEN_WIDTH // self.tile, (SCREEN_HEIGHT - 75) // self.tile
        self.map_width = SCREEN_WIDTH // self.tile * self.tile
        self.map_height = (SCREEN_HEIGHT - 75) // self.tile * self.tile
        # отображение побед
        self.overlay = Overlay(self.screen)
        self.blue_wins = 0
        self.red_wins = 0
        self.round = 0
        self.overlay.timers["animation"].freeze = True
        # спрайты
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        # генерация
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid_cells.append(Cell(self.screen, x, y, self.tile, self.cols, self.rows))
        # Таймер
        self.timers = {
            "wait round": Timer(500, lambda: self.change_score())
        }
        self.timers["wait round"].freeze = True

        self.new_lvl()

    def new_lvl(self):
        self.overlay.start_animation()
        self.generation()
        self.setup()

    def generation(self):
        self.round += 1
        self.stack.clear()
        for wall in self.walls:
            wall.kill()

        for cell in self.grid_cells:
            cell.walls['top'] = True
            cell.walls['right'] = True
            cell.walls['bottom'] = True
            cell.walls['left'] = True
            cell.visited = False

        # Генерация стенок лабиринта
        current_cell = self.grid_cells[0]
        next_cell = current_cell.check_neighbors(self.grid_cells)
        while next_cell or self.stack:
            if next_cell:
                next_cell.visited = True
                self.stack.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif self.stack:
                current_cell = self.stack.pop()
            next_cell = current_cell.check_neighbors(self.grid_cells)

        # Уменьшение кол-ва стенок
        # for cell in self.grid_cells:
        #     next_cell = check_neighbors_second(cell, self.grid_cells)
        #     remove_walls(cell, next_cell)

        # Создание стен
        for cell in self.grid_cells:
            x = cell.x * self.tile
            y = cell.y * self.tile
            if cell.walls['top']:
                Border(x, y, x + self.tile, y, self.all_sprites, self.walls)
            if cell.walls['right']:
                Border(x + self.tile, y, x + self.tile, y + self.tile, self.all_sprites, self.walls)
            if cell.walls['bottom']:
                Border(x, y + self.tile, x + self.tile, y + self.tile, self.all_sprites, self.walls)
            if cell.walls['left']:
                Border(x, y, x, y + self.tile, self.all_sprites, self.walls)

    def change_score(self):
        self.timers["wait round"].freeze = True
        if self.player_sprites.sprites():
            if self.player_sprites.sprites()[0].player_number == 1:
                self.blue_wins += 1
            elif self.player_sprites.sprites()[0].player_number == 2:
                self.red_wins += 1
            self.player_sprites.sprites()[0].kill()
        self.new_lvl()

    def setup(self):
        flag = True
        while flag:
            pos1, pos2, vec1, vec2 = self.set_position()
            Player(self, self.settings, pos1, vec1, 1, self.all_sprites, self.player_sprites, self.walls)
            Player(self, self.settings, pos2, vec2, 2, self.all_sprites, self.player_sprites, self.walls)
            pygame.sprite.groupcollide(self.player_sprites, self.walls, True, False)
            if len(self.player_sprites) == 2:
                flag = False
            else:
                for player in self.player_sprites:
                    player.kill()

    def set_position(self):
        x1 = randint(50, self.map_width // 2 - 25)
        y1 = randint(50, self.map_height - 50)
        x2 = randint(self.map_width // 2 + 25, self.map_width - 50)
        y2 = randint(50, self.map_height - 50)
        vec1 = (uniform(-1, 1), uniform(-1, 1))
        vec2 = (uniform(-1, 1), uniform(-1, 1))
        return (x1, y1), (x2, y2), vec1, vec2

    def run(self, dt):
        self.screen.fill(WHITE)
        for cell in self.grid_cells:
            cell.draw()
        self.overlay.display(self.round, self.blue_wins, self.red_wins)
        self.overlay.update_timers()
        self.all_sprites.draw(self.screen)
        self.all_sprites.update(dt)
        self.update_timers()

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
