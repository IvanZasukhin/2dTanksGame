import sys
import pygame
from level import Level

from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Game')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            pygame.display.update()
            pygame.display.set_caption("FPS: " + str(int(self.clock.get_fps())))  # FPS


if __name__ == '__main__':
    game = Game()
    game.run()
