from map import *
from player import Player
from settings import *
from support import remove_walls
from random import randint


class Level:
    def __init__(self, screen):
        # окно
        self.display_surface = screen

        self.grid_cells = []
        self.stack = []
        self.tile = 200
        self.cols, self.rows = SCREEN_WIDTH // self.tile, SCREEN_HEIGHT // self.tile
        # спрайты
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.generation()
        self.setup()

    def generation(self):
        # Создание клеток
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid_cells.append(Cell(self.display_surface, x, y, self.tile, self.cols, self.rows))

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

        # Создание спрайта стен
        for cell in self.grid_cells:
            x = cell.x * self.tile
            y = cell.y * self.tile
            if cell.walls['top']:
                Border(self.all_sprites, self.walls, self.collision_sprites, x, y,
                       x + self.tile, y)
            if cell.walls['right']:
                Border(self.all_sprites, self.walls, self.collision_sprites, x + self.tile,
                       y, x + self.tile, y + self.tile)
            if cell.walls['bottom']:
                Border(self.all_sprites, self.walls, self.collision_sprites, x,
                       y + self.tile, x + self.tile, y + self.tile)
            if cell.walls['left']:
                Border(self.all_sprites, self.walls, self.collision_sprites, x, y, x,
                       y + self.tile)

    def setup(self):
        flag = True
        while flag:
            pos1, pos2 = self.set_position()
            print(pos1, pos2)
            Player(pos1, 1, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites,
                   self.v_walls, self.h_walls)
            Player(pos2, 2, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites,
                   self.v_walls, self.h_walls)
            pygame.sprite.groupcollide(self.player_sprites, self.walls, True, False)
            if len(self.player_sprites) == 2:
                flag = False
            else:
                for player in self.player_sprites:
                    player.kill()

    def set_position(self):
        width = SCREEN_WIDTH // self.tile * self.tile
        height = SCREEN_HEIGHT // self.tile * self.tile
        x1 = randint(50, width // 2 - 25)
        y1 = randint(50, height - 50)
        x2 = randint(width // 2 + 25, width - 50)
        y2 = randint(50, height - 50)
        return (x1, y1), (x2, y2)

    def run(self, dt):
        self.display_surface.fill(WHITE)
        for cell in self.grid_cells:
            cell.draw()
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
