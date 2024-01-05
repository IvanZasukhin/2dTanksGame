from map import *
from player import Player
from settings import *
from support import remove_walls
from random import randint


class Level:
    def __init__(self, screen):
        # окно
        self.display_surface = screen
        # карта
        self.grid_cells = []
        self.stack = []
        self.tile = 225
        self.cols, self.rows = SCREEN_WIDTH // self.tile, (SCREEN_HEIGHT - 75) // self.tile
        self.map_width = SCREEN_WIDTH // self.tile * self.tile
        self.map_height = (SCREEN_HEIGHT - 75) // self.tile * self.tile
        # отображение побед
        self.font_name = pygame.font.match_font('arial')
        self.blue_wins = 0
        self.red_wins = 0
        self.round = 0
        # спрайты
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        # генерация
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid_cells.append(Cell(self.display_surface, x, y, self.tile, self.cols, self.rows))
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
                Border(x, y, x + self.tile, y, self.all_sprites, self.walls, self.collision_sprites)
            if cell.walls['right']:
                Border(x + self.tile, y, x + self.tile, y + self.tile, self.all_sprites, self.walls,
                       self.collision_sprites)
            if cell.walls['bottom']:
                Border(x, y + self.tile, x + self.tile, y + self.tile, self.all_sprites, self.walls,
                       self.collision_sprites)
            if cell.walls['left']:
                Border(x, y, x, y + self.tile, self.all_sprites, self.walls, self.collision_sprites)

    def draw_text(self, text, color, x, y):
        font = pygame.font.Font(self.font_name, 48)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.display_surface.blit(text_surface, text_rect)

    def change_score(self):
        if self.player_sprites.sprites()[0].player_number == 1:
            self.blue_wins += 1
        else:
            self.red_wins += 1
        self.player_sprites.sprites()[0].kill()
        self.generation()
        self.setup()

    def setup(self):
        flag = True
        while flag:
            pos1, pos2 = self.set_position()
            Player(self, pos1, 1, self.all_sprites, self.player_sprites, self.collision_sprites,
                   self.walls)
            Player(self, pos2, 2, self.all_sprites, self.player_sprites, self.collision_sprites,
                   self.walls)
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
        return (x1, y1), (x2, y2)

    def run(self, dt):
        self.display_surface.fill(WHITE)
        for cell in self.grid_cells:
            cell.draw()
        self.draw_text(f'BLUE: {self.blue_wins}', BLUE, 110, self.map_height + 10)
        self.draw_text(f'RED: {self.red_wins}', RED, self.map_width - 100, self.map_height + 10)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
