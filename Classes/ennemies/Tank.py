import os
import pygame
from Classes.Character import Character
from Classes.Bullet import Bullet
from Classes.SoundManager import SoundManager

bulletImage = pygame.image.load('assets/ennemies/tank/bullet.png')


class Tank(Character):
    soundManager = SoundManager()
    soundManager.load_sounds({
        'shooting': 'assets/ennemies/tank/fx/shooting.wav'
    })
    shooting = [pygame.image.load(os.path.join(
        'assets/ennemies/tank/shooting/', 'tile' + str(x) + '.png')) for x in range(0, 10)]

    moving = [pygame.image.load(os.path.join(
        'assets/ennemies/tank/moving', 'tile' + str(x) + '.png')) for x in range(1, 2)]

    exploding = [pygame.image.load(os.path.join(
        'assets/ennemies/tank/exploding', 'tile' + str(x) + '.png')) for x in range(0, 11)]

    def __init__(self, x, containerHeight, width, height, direction):
        self.defaultY = containerHeight - \
            (self.shooting[0].get_size()[1] * 4.5)
        self.width = width
        self.height = (self.shooting[0].get_size()[1] * 4.5)
        self.direction = direction
        self.moveCount = 0
        self.moving_speed = 0.5
        self.bullets = []
        self.isExploding = False
        self.cooldown = 2500
        self.lastShoot = pygame.time.get_ticks()

        Character.__init__(self, 100, 10, 8, x, self.defaultY,
                           self.shooting[0].get_size())

    def draw(self, win):
        self.lifeBar.update(win, self.x, self.y + 100, self.health)
        self.shoot()
        for bullet in self.bullets:
            if bullet.x == bullet.baseX:
                self.soundManager.play_sound('shooting', True)
            bullet.move()
            bullet.draw(win)

        if self.isExploding:
            self.die(win)
        else:
            win.blit(Character.rotate(Character.scale(
                self.moving[self.moveCount - 1], 4.5), self.direction), (self.x, self.y))

    def handle_move(self, keys, backgroundSpeed):
        if not self.isExploding:
            if self.moveCount > len(self.moving) - 1:
                self.moveCount = 0
            self.x += self.moving_speed if self.direction == pygame.K_LEFT else (
                self.moving_speed) * -1

            # permet de garder la position du tank synchronisée avec le background
            if keys[pygame.K_LEFT]:
                self.x += backgroundSpeed
            if keys[pygame.K_RIGHT]:
                self.x -= backgroundSpeed

            self.moveCount += 1

    # shoot every 4 seconds

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShoot > self.cooldown:
            self.lastShoot = now
            self.bullets.append(
                Bullet(self.x + self.width, self.y + self.height / 2, 40, 30, bulletImage, self.direction, 2.5))

        for bullet in self.bullets:
            if bullet.x <= 0:
                self.bullets.pop(self.bullets.index(bullet))

    def die(self, win):
        if not self.isExploding:
            self.moveCount = 0
            self.isExploding = True

        win.blit(Character.scale(
            self.exploding[self.moveCount], 4.5), (self.x, self.y))
        self.moveCount += 1
        if self.moveCount > len(self.exploding) - 1:
            self.moveCount = 0
            self.isExploding = False
