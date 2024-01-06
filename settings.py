from pygame import Color, K_LEFT, K_DOWN, K_a, K_s, K_RIGHT, K_KP0, K_d, K_e, K_w, K_UP

BLACK = Color('black')
ORANGE = Color('orange')
RED = Color('red')
BLUE = Color('blue')
WHITE = Color('white')
GRAY = Color('gray')
PLAYER_ZOOM = 0.125
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (900, 975)
MANAGEMENT = {
    1: {"left": K_a, "right": K_d, "up": K_w,
        "down": K_s, "attack": K_e},
    2: {"left": K_LEFT, "right": K_RIGHT, "up": K_UP,
        "down": K_DOWN, "attack": K_KP0}}
