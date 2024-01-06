from pygame import font
from settings import *
from timer import Timer


class Overlay:
    def __init__(self, screen):
        self.screen = screen
        self.font_name = font.match_font('arial')
        self.digit = 3
        self.stop_game = False
        self.timers = {
            "animation": Timer(500),
        }

    def draw_text(self, text, color, x, y):
        fonts = font.Font(self.font_name, 48)
        text_surface = fonts.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midbottom = (x, y)
        self.screen.blit(text_surface, text_rect)

    def display(self, round, blue_wins, red_wins):
        self.draw_text(f'BLUE: {blue_wins}', BLUE, 100, self.screen.get_height())
        self.draw_text(f'RED: {red_wins}', RED, self.screen.get_width() - 100, self.screen.get_height())
        self.draw_text(f'ROUND: {round}', BLACK, self.screen.get_width() // 2, self.screen.get_height())

    def animation(self):
        fonts = font.Font(self.font_name, 200)
        text_surface = fonts.render(str(self.digit), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.screen.blit(text_surface, text_rect)

    def start_animation(self):
        self.digit = 3
        self.stop_game = False
        self.timers["animation"].activate()

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def check_animation(self):
        if self.timers["animation"].active:
            self.animation()
        else:
            if self.digit != 1:
                self.digit -= 1
                self.timers["animation"].activate()
            else:
                self.stop_game = True
        return self.stop_game
