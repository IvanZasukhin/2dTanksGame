from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, player_number, walls, all_sprites, player_sprites):
        super().__init__(all_sprites, player_sprites)
        self.all_sprites = all_sprites
        self.player_sprites = player_sprites
        self.walls = walls
        self.MANAGEMENT = {
            1: {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP,
                "down": pygame.K_DOWN, "attack": pygame.K_SPACE},
            2: {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w,
                "down": pygame.K_s, "attack": pygame.K_e}}[player_number]
        # Генерация изображения
        self.animations = {"stop": [], "forward": [], "left": [], "right": []}
        self.status = "stop"
        self.speed_animation = 15
        self.frame = 0
        self.import_animation()

        self.image = self.animations[self.status][self.frame]
        self.orig_image = self.animations[self.status][self.frame]
        self.rect = self.image.get_rect(center=pos)
        # Движение

        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2((0, -1))
        self.speed = 1
        self.speed_angle = 0.5
        # Таймер
        self.timers = {
            "attack": Timer(360)
        }

    def import_animation(self):
        for animation in self.animations.keys():
            full_path = "data/animations/standard/" + animation
            self.animations[animation] = import_image(full_path)

    def input(self, dt):
        keys = pygame.key.get_pressed()
        # поворот танка
        movement = 0
        self.speed_animation = 15
        self.status = "stop"
        if keys[self.MANAGEMENT["up"]]:
            self.status = "forward"
            movement = -1
        elif keys[self.MANAGEMENT["down"]]:
            self.status = "forward"
            movement = 1

        direction_old = self.direction
        if keys[self.MANAGEMENT["left"]]:
            self.speed_animation = 30
            self.status = "left"
            self.direction = self.direction.rotate(dt * -360 * self.speed_angle)
        elif keys[self.MANAGEMENT["right"]]:
            self.speed_animation = 30
            self.status = "right"
            self.direction = self.direction.rotate(dt * 360 * self.speed_angle)

        # движение танка
        movement_v = self.direction * movement
        if movement_v.length() > 0:
            movement_v.normalize_ip()
            self.pos += movement_v * dt * 100 * self.speed
        # TODO: проблема, если танк заезжает в другой танк на пиксель то он застревает надо
        #  чтобы после столкновения так отъезжал на 1 пиксель а так же улучшить систему сталкивания
        for sprite in self.player_sprites:
            if not (sprite is self):
                if pygame.sprite.collide_mask(self, sprite):
                    self.pos -= movement_v * dt * 100 * self.speed
                    sprite.collision(dt, movement_v)
                    self.direction = direction_old
        # атака
        if keys[self.MANAGEMENT["attack"]]:
            print("attack")

    def update(self, dt):
        self.input(dt)
        self.animation(dt)

    def animation(self, dt):
        self.frame += self.speed_animation * dt
        if self.frame >= len(self.animations[self.status]):
            self.frame = 0
        self.image = self.animations[self.status][int(self.frame)]
        self.image = pygame.transform.rotate(self.animations[self.status][int(self.frame)],
                                             self.direction.angle_to((0, -1)))
        self.rect = self.image.get_rect(center=self.pos)

    def collision(self, dt, movement_v):
        self.pos += movement_v * dt * 100 * self.speed
