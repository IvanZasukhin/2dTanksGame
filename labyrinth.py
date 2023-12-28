import pygame
from random import choice, randint

RES = WIDTH, HEIGHT = 800, 800
TILE = 100
ORANGE = pygame.Color('darkorange')
BLACK = pygame.Color('black')
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
v_walls = pygame.sprite.Group()
h_walls = pygame.sprite.Group()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, BLACK, (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(screen, ORANGE, (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(screen, ORANGE, (x + TILE, y), (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(screen, ORANGE, (x + TILE, y + TILE), (x, y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(screen, ORANGE, (x, y + TILE), (x, y), 3)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
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
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(v_walls)
            self.image = pygame.Surface([3, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 3, y2 - y1)
        else:  # горизонтальная стенка
            self.add(h_walls)
            self.image = pygame.Surface([x2 - x1, 3])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 3)


def check_neighbors_second(cell):
    self = cell
    neighbors = []
    top = self.check_cell(self.x, self.y - 1)
    right = self.check_cell(self.x + 1, self.y)
    bottom = self.check_cell(self.x, self.y + 1)
    left = self.check_cell(self.x - 1, self.y)
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


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


# Создание клеток
grid_cells = []
for row in range(rows):
    for col in range(cols):
        grid_cells.append(Cell(col, row))

# Генерация стенок лабиринта
current_cell = grid_cells[0]
next_cell = current_cell.check_neighbors()
stack = []
while next_cell or stack:
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
    next_cell = current_cell.check_neighbors()

# Уменьшение кол-ва стенок
for cell in grid_cells:
    count = randint(0, 3)
    for _ in range(count):
        next_cell = check_neighbors_second(cell)
        remove_walls(cell, next_cell)

# Создание спрайта стен
for cell in grid_cells:
    x = cell.x
    y = cell.y
    if cell.walls['top']:
        Border(x, y, x + TILE, y)
    if cell.walls['right']:
        Border(x + TILE, y, x + TILE, y + TILE)
    if cell.walls['bottom']:
        Border(x, y + TILE, x + TILE, y + TILE)
    if cell.walls['left']:
        Border(x, y, x, y + TILE)


# Основной цикл
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    [cell.draw() for cell in grid_cells]

    pygame.display.flip()
    clock.tick(60)
