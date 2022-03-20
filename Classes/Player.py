import pygame
import os

from Classes.Bullet import Bullet
from Classes.Character import Character
from Classes.SoundManager import SoundManager

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

bulletImage = pygame.image.load('assets/player/bullet.png')


class Player(Character):
    soundManager = SoundManager()
    soundManager.load_sounds({
        'running': 'assets/player/fx/running.wav',
        'shooting': 'assets/ennemies/tank/fx/shooting.wav'
    })
    run = [pygame.image.load(os.path.join('images', str(x) + '.png'))
           for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join(
        'images', str(x) + '.png')) for x in range(1, 8)]

    def __init__(self, x, containerHeight, width, height, direction):
        self.defaultY = containerHeight - (self.jump[0].get_size()[1] * 4.5)
        self.width = width
        self.height = self.jump[0].get_size()[1] * 4.5
        self.jumping = False
        self.direction = direction
        self.jumpCount = 10
        self.runCount = 0
        self.score = 0
        self.bullets = []
        self.countdown = 300
        self.health = 100
        self.lastShot = pygame.time.get_ticks()
        Character.__init__(self, 100, 10, 8, x, self.defaultY,
                           self.jump[0].get_size())

    def draw(self, win):
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(win)
        if self.jumping:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 1 * neg
                self.jumpCount -= 1
            else:
                self.jumping = False
                self.jumpCount = 10

            win.blit(Character.scale(
                Character.rotate(self.jump[self.jumpCount // 18 * -1], self.direction), 2.6), (self.x, self.y))

        if self.runCount > 42:
            self.runCount = 0
        if not self.jumping:
            win.blit(Character.rotate(Character.scale(
                self.run[self.runCount//6], 2.6), self.direction), (self.x, self.y))
            self.hitbox = (self.x + 4, self.y, self.width-24, self.height-13)

        self.lifeBar.update(win, self.x, self.y, self.health)
        textsurface = myfont.render(
            "Score " + str(self.score), False, (255, 255, 255))
        win.blit(textsurface, (10, 10))

    # gérer les touches appuyées

    def handleKeyPress(self, keys):
        if keys[pygame.K_UP]:
            self.jumping = True
        if keys[pygame.K_SPACE]:
            self.shoot()

        if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and ((keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]) or (not keys[pygame.K_RIGHT] and keys[pygame.K_LEFT])):
            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.direction = pygame.K_LEFT
                if self.direction != pygame.K_RIGHT:
                    self.runCount += 1
                else:
                    self.runCount = 0

            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.direction = pygame.K_RIGHT
                if self.direction != pygame.K_LEFT:
                    self.runCount += 1
                else:
                    self.runCount = 0
            if(self.runCount > 0):
                self.soundManager.play_sound('running')
            else:
                self.soundManager.stop_sound('running')
        else:
            self.soundManager.stop_sound('running')

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShot >= self.countdown:
            self.lastShot = now
            self.bullets.append(
                Bullet(self.x, self.y + self.height * 0.3, 40, 20, bulletImage, pygame.K_RIGHT if self.direction == pygame.K_LEFT else pygame.K_LEFT, 10))
            self.soundManager.play_sound('shooting', True)

    def increaseScore(self, value):
        self.score += value
