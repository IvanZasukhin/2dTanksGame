import pygame.sprite
from random import choice

from pygame import draw
from constants import *


class Cell:
    def __init__(self, screen, x, y, tile, cols, rows):
        self.screen = screen
        self.x, self.y = x, y
        self.walls = {}
        self.visited = False
        self.TILE = tile
        self.cols, self.rows = cols, rows

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
    def __init__(self, x1, y1, x2, y2, *groups):
        super().__init__(*groups)
        thickness = 10
        x1, y1 = x1 - thickness / 2, y1 - thickness / 2
        x2, y2 = x2 - thickness / 2, y2 - thickness / 2

        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([thickness, y2 - y1 + thickness], pygame.SRCALPHA)
            pygame.draw.rect(self.image, BLACK, (0, 0, thickness, y2 - y1 + thickness))
        elif y1 == y2:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1 + thickness, thickness], pygame.SRCALPHA)
            pygame.draw.rect(self.image, BLACK, (0, 0, x2 - x1 + thickness, thickness))

        self.rect = self.image.get_rect(topleft=(x1, y1))
        self.direction = -pygame.Vector2(x2 - x1, y2 - y1).rotate(90).normalize()
        self.mask = pygame.mask.from_surface(self.image)

    def is_collided_with(self, sprite):
        return pygame.sprite.collide_mask(self, sprite)


