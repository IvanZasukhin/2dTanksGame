from pygame import time


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.freeze = False

    def activate(self):
        self.active = True
        self.freeze = False
        self.start_time = time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = time.get_ticks()
        if current_time - self.start_time >= self.duration and not self.freeze:
            self.deactivate()
            if self.func:
                self.func()
