from map import *
from player import Player


class Level:
    def __init__(self, screen):
        # окно
        self.display_surface = screen

        self.grid_cells = []
        self.stack = []
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
        for row in range(rows):
            for col in range(cols):
                self.grid_cells.append(Cell(self.display_surface, col, row))

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
            x = cell.x
            y = cell.y
            if cell.walls['top']:
                Border(self.all_sprites, self.collision_sprites, x, y, x + TILE, y)
            if cell.walls['right']:
                Border(self.all_sprites, self.collision_sprites, x + TILE, y, x + TILE, y + TILE)
            if cell.walls['bottom']:
                Border(self.all_sprites, self.collision_sprites, x, y + TILE, x + TILE, y + TILE)
            if cell.walls['left']:
                Border(self.all_sprites, self.collision_sprites, x, y, x, y + TILE)

    def setup(self):
        Player((300, 300), 1, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites)
        Player((400, 300), 2, (self.all_sprites, self.player_sprites), self.collision_sprites, self.bullet_sprites)

    def run(self, dt):
        self.display_surface.fill(BLACK)
        for cell in self.grid_cells:
            cell.draw()
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
