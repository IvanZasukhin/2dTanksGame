from pygame import Color, K_LEFT, K_DOWN, K_a, K_s, K_RIGHT, K_RCTRL, K_d, K_e, K_w, K_UP
from pygame_menu import themes

BLACK = Color('black')
ORANGE = Color('orange')
RED = Color('red')
BLUE = Color('blue')
WHITE = Color('white')
GRAY = Color('gray')
DARKGRAY = Color("darkgray")
MY_THEME = themes.THEME_DEFAULT.copy()
MY_THEME.selection_color = BLACK
MY_THEME.widget_selection_effect.set_background_color(DARKGRAY)
PLAYER_ZOOM = 0.125
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (875, 775)
MANAGEMENT = {
    1: {"left": K_a, "right": K_d, "up": K_w,
        "down": K_s, "attack": K_e},
    2: {"left": K_LEFT, "right": K_RIGHT, "up": K_UP,
        "down": K_DOWN, "attack": K_RCTRL}}
