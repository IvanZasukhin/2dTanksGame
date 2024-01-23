def get_settings():
    with open('data/settings.txt') as file:
        return [int(line.strip()) for line in file.readlines()]


def remove_walls(current, next_walls):
    dx = current.x - next_walls.x
    if dx == 1:
        current.walls['left'] = False
        next_walls.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next_walls.walls['left'] = False
    dy = current.y - next_walls.y
    if dy == 1:
        current.walls['top'] = False
        next_walls.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next_walls.walls['top'] = False
