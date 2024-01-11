from pygame import Color, K_LEFT, K_DOWN, K_a, K_s, K_RIGHT, K_RCTRL, K_d, K_LSHIFT, K_w, K_UP
from pygame_menu import themes

BLACK = Color('black')
ORANGE = Color('orange')
RED = Color('red')
BLUE = Color('blue')
WHITE = Color('white')
GRAY = Color('gray')
DARKGRAY = Color("darkgray")
GREEN = Color('green')
PURPLE = Color('purple')

MY_THEME = themes.THEME_DEFAULT.copy()
MY_THEME.selection_color = BLACK
MY_THEME.widget_selection_effect.set_background_color(DARKGRAY)

PLAYER_SCALE = 0.125
PLAYER_MAX_SPEED = 200

RADIUS_BULLET = 9
BULLET_SPEED_COF = 1.5
TIME_LIFE_BULLET = 10000

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (875, 775)
MANAGEMENT = {
    1: {"left": K_a, "right": K_d, "up": K_w,
        "down": K_s, "attack": K_LSHIFT},
    2: {"left": K_LEFT, "right": K_RIGHT, "up": K_UP,
        "down": K_DOWN, "attack": K_RCTRL}}
