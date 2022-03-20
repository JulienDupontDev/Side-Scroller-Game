import pygame


class LifeBar(object):
    def __init__(self, x, y, size, value):
        self.updatePosition(x, y)
        self.size = size
        self.value = value

    def draw(self, win):
        lifebar_background = pygame.Surface((self.size, 10))
        lifebar_background.set_alpha(128)
        lifebar_background.fill((255, 255, 255))
        win.blit(lifebar_background, (self.x, self.y))

        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.value, 10))

    def update(self, win, x, y, value):
        self.value = value
        self.updatePosition(x, y)
        if self.value > self.size:
            self.value = self.size
        if self.value < 0:
            self.value = 0
        self.draw(win)

    def updatePosition(self, x, y):
        self.x = x
        self.y = y - 15
