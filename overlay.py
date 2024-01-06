import pygame
from settings import *


class Overlay:
    def __init__(self, screen):
        self.screen = screen
        self.font_name = pygame.font.match_font('arial')
        self.font = pygame.font.Font(self.font_name, 48)

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midbottom = (x, y)
        self.screen.blit(text_surface, text_rect)

    def display(self, round, blue_wins, red_wins):
        self.draw_text(f'BLUE: {blue_wins}', BLUE, 100, self.screen.get_height())
        self.draw_text(f'RED: {red_wins}', RED, self.screen.get_width() - 100, self.screen.get_height())
        self.draw_text(f'ROUND: {round}', BLACK, self.screen.get_width() // 2, self.screen.get_height())
