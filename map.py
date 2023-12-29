import pygame
from settings import *
from random import choice


class Cell:
    def __init__(self, screen, x, y, tile, cols, rows):
        self.screen = screen
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.TILE = tile
        self.cols, self.rows = cols, rows

    def draw(self):
        x, y = self.x * self.TILE, self.y * self.TILE
        if self.visited:
            pygame.draw.rect(self.screen, pygame.Color("gray"), (x, y, self.TILE, self.TILE))
        if self.walls['top']:
            pygame.draw.line(self.screen, ORANGE, (x, y), (x + self.TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(self.screen, ORANGE, (x + self.TILE, y), (x + self.TILE, y + self.TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(self.screen, ORANGE, (x, y + self.TILE), (x + self.TILE, y + self.TILE), 3)
        if self.walls['left']:
            pygame.draw.line(self.screen, ORANGE, (x, y), (x, y + self.TILE), 3)

    def check_cell(self, grid_cells, x, y):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        return grid_cells[x + y * self.cols]

    def check_neighbors(self, grid_cells):
        neighbors = []
        top = self.check_cell(grid_cells, self.x, self.y - 1)
        right = self.check_cell(grid_cells, self.x + 1, self.y)
        bottom = self.check_cell(grid_cells, self.x, self.y + 1)
        left = self.check_cell(grid_cells, self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        if neighbors:
            return choice(neighbors)
        else:
            return False


class Border(pygame.sprite.Sprite):
    def __init__(self, all_sprites, v_walls, h_walls, collision_sprites, x1, y1, x2, y2):
        super().__init__(all_sprites, collision_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(v_walls)
            self.image = pygame.Surface([3, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 3, y2 - y1)
        else:  # горизонтальная стенка
            self.add(h_walls)
            self.image = pygame.Surface([x2 - x1, 3])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 3)
        self.mask = pygame.mask.from_surface(self.image)

    def is_collided_with(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)


def check_neighbors_second(cell, grid_cells):
    neighbors = []
    top = cell.check_cell(grid_cells, cell.x, cell.y - 1)
    right = cell.check_cell(grid_cells, cell.x + 1, cell.y)
    bottom = cell.check_cell(grid_cells, cell.x, cell.y + 1)
    left = cell.check_cell(grid_cells, cell.x - 1, cell.y)
    if top:
        neighbors.append(top)
    if right:
        neighbors.append(right)
    if bottom:
        neighbors.append(bottom)
    if left:
        neighbors.append(left)
    if neighbors:
        return choice(neighbors)
    else:
        return False