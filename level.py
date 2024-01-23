from map import *
from support import remove_walls
from random import randint, uniform, choice
from support import get_settings
from player import Player
from timer import Timer
from overlay import Overlay
from upgrades import *


class Level1:
    def __init__(self, game):
        self.game = game
        self.settings = get_settings()
        # окно
        self.screen = pygame.display.get_surface()
        self.settings_menu = None
        # карта
        self.grid_cells = []
        self.stack = []
        self.tile = 175
        self.boost_types = ('speed boost', 'attack boost')
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
        self.boost_sprites = pygame.sprite.Group()
        # генерация
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid_cells.append(Cell(self.screen, x, y, self.tile, self.cols, self.rows))
        # Таймер
        self.timers = {
            "wait round": Timer(500, lambda: self.change_score())
        }
        self.timers["wait round"].freeze = True

        self.freeze = False
        self.new_lvl()

    def new_lvl(self):
        for sprite in self.all_sprites:
            sprite.kill()
        self.generation()
        self.setup()
        self.overlay.start_animation()

    def generation(self):
        self.round += 1
        self.stack.clear()

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
        if self.round == self.settings[2]:
            pygame.display.quit()
            self.game.end_game(self.blue_wins, self.red_wins)
        self.new_lvl()

    def setup(self):
        upgrades_count = randint(2, 5)
        for i in range(upgrades_count):
            boost = None
            pos = self.set_upgrade_position()
            boost_type = choice(self.boost_types)
            if boost_type == 'speed boost':
                boost = SpeedBoost(pos, self.player_sprites, self.all_sprites, self.boost_sprites)
            elif boost_type == 'attack boost':
                boost = AttackBoost(pos, self.player_sprites, self.all_sprites, self.boost_sprites)

            if pygame.sprite.spritecollide(boost, self.walls, False):
                boost.kill()
            if pygame.sprite.spritecollide(boost, self.player_sprites, False):
                boost.kill()

        flag = True
        while flag:
            pos1, pos2, vec1, vec2 = self.set_players_positions()
            Player(self, self.settings, pos1, vec1, 1,
                   self.walls, self.boost_sprites, self.all_sprites, self.player_sprites)
            Player(self, self.settings, pos2, vec2, 2,
                   self.walls, self.boost_sprites, self.all_sprites, self.player_sprites)
            pygame.sprite.groupcollide(self.player_sprites, self.walls, True, False)
            if len(self.player_sprites) == 2:
                flag = False
            else:
                for player in self.player_sprites:
                    player.kill()

    def set_players_positions(self):
        x1 = randint(50, self.map_width // 2 - 25)
        y1 = randint(50, self.map_height - 50)
        x2 = randint(self.map_width // 2 + 25, self.map_width - 50)
        y2 = randint(50, self.map_height - 50)
        vec1 = (uniform(-1, 1), uniform(-1, 1))
        vec2 = (uniform(-1, 1), uniform(-1, 1))
        return (x1, y1), (x2, y2), vec1, vec2

    def set_upgrade_position(self):
        x = randint(25, self.map_width - 25)
        y = randint(25, self.map_height - 25)
        return x, y

    def run(self, dt):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, GRAY, (0, 0, self.cols * self.tile, self.rows * self.tile))
        self.overlay.display(self.round, self.blue_wins, self.red_wins)
        self.all_sprites.draw(self.screen)
        if self.freeze:
            dt = 0
            self.resume_game()
        self.all_sprites.update(dt)
        self.overlay.update_timers()
        self.update_timers()

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def pause_game(self):
        self.freeze = True
        for sprite in self.all_sprites.sprites():
            if hasattr(sprite, "timers"):
                for i in sprite.timers:
                    sprite.timers[i].pause()

    def resume_game(self):
        self.freeze = False
        for sprite in self.all_sprites.sprites():
            if hasattr(sprite, "timers"):
                for i in sprite.timers:
                    sprite.timers[i].resume()


class Level2(Level1):
    def generation(self):
        self.round += 1
        self.stack.clear()
        Border(0, 0, 0, self.rows * self.tile, self.all_sprites, self.walls)
        Border(0, 0, self.cols * self.tile, 0, self.all_sprites, self.walls)
        Border(self.cols * self.tile, 0, self.cols * self.tile, self.rows * self.tile, self.all_sprites, self.walls)
        Border(0, self.rows * self.tile, self.cols * self.tile, self.rows * self.tile, self.all_sprites, self.walls)

    def setup(self):
        upgrades_count = randint(2, 5)
        for i in range(upgrades_count):
            boost = None
            pos = self.set_upgrade_position()
            boost_type = choice(self.boost_types)
            if boost_type == 'speed boost':
                boost = SpeedBoost(pos, self.player_sprites, self.all_sprites, self.boost_sprites)
            elif boost_type == 'attack boost':
                boost = AttackBoost(pos, self.player_sprites, self.all_sprites, self.boost_sprites)

            if pygame.sprite.spritecollide(boost, self.walls, False):
                boost.kill()
            if pygame.sprite.spritecollide(boost, self.player_sprites, False):
                boost.kill()

        Player(self, self.settings, (self.map_width / 4, self.map_height / 2), (-1, 0),
               1, self.walls, self.boost_sprites, self.all_sprites, self.player_sprites)
        Player(self, self.settings, (self.map_width / 1.25, self.map_height / 2), (1, 0),
               2, self.walls, self.boost_sprites, self.all_sprites, self.player_sprites)

