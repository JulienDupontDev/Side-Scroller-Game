import pygame

from random import randrange


class Bullet(object):
    def __init__(self, x, y, width, height, image, direction, damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = 5
        self.baseX = x
        self.damage = damage
        self.image = pygame.transform.scale(pygame.transform.rotate(
            image, 0 if self.direction == pygame.K_LEFT else 180), (self.width, self.height))

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.move()

    def move(self):
        if self.direction == pygame.K_LEFT:
            self.x += self.speed
        elif self.direction == pygame.K_RIGHT:
            self.x -= self.speed
