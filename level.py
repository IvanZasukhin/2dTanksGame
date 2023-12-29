from map import *
from player import Player
from support import remove_walls


class Level:
    def __init__(self, screen):
        # окно
        self.display_surface = screen

        self.grid_cells = []
        self.stack = []
        self.TILE = 200
        self.cols, self.rows = SCREEN_WIDTH // self.TILE, SCREEN_HEIGHT // self.TILE
        # спрайты
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.v_walls = pygame.sprite.Group()
        self.h_walls = pygame.sprite.Group()

        self.generation()
        self.setup()

    def generation(self):
        # Создание клеток
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid_cells.append(Cell(self.display_surface, x, y, self.TILE, self.cols, self.rows))

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
        for cell in self.grid_cells:
            next_cell = check_neighbors_second(cell, self.grid_cells)
            remove_walls(cell, next_cell)

        # Создание спрайта стен
        for cell in self.grid_cells:
            x = cell.x * self.TILE
            y = cell.y * self.TILE
            if cell.walls['top']:
                Border(self.all_sprites, self.v_walls, self.h_walls, self.collision_sprites, x, y, x + self.TILE, y)
            if cell.walls['right']:
                Border(self.all_sprites, self.v_walls, self.h_walls, self.collision_sprites, x + self.TILE, y,
                       x + self.TILE, y + self.TILE)
            if cell.walls['bottom']:
                Border(self.all_sprites, self.v_walls, self.h_walls, self.collision_sprites, x, y + self.TILE,
                       x + self.TILE, y + self.TILE)
            if cell.walls['left']:
                Border(self.all_sprites, self.v_walls, self.h_walls, self.collision_sprites, x, y, x, y + self.TILE)

    def setup(self):
        Player((300, 300), 1, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites,
               self.v_walls, self.h_walls)
        Player((400, 300), 2, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites,
               self.v_walls, self.h_walls)

    def run(self, dt):
        self.display_surface.fill(WHITE)
        for cell in self.grid_cells:
            cell.draw()
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
