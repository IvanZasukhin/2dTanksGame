from pygame import Color, K_LEFT, K_DOWN, K_a, K_s, K_RIGHT, K_SPACE, K_d, K_e, K_w, K_UP

FPS = 50
BLACK = Color('black')
RED = Color('red')
BLUE = Color('blue')
WHITE = Color('white')
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (600, 600)
MANAGEMENT = {
    1: {"left": K_LEFT, "right": K_RIGHT, "up": K_UP,
        "down": K_DOWN, "attack": K_SPACE},
    2: {"left": K_a, "right": K_d, "up": K_w,
        "down": K_s, "attack": K_e}}

