import os
from random import randrange
import pygame
import time as t
from Classes.Background import Background
from Classes.Character import Character
from Classes.Player import Player
from Classes.ennemies.Tank import Tank

# largeFont = pygame.font.SysFont('comicsans', 80)


class Scene(object):

    def __init__(self, surface):
        self.bg_image = pygame.image.load(os.path.join(
            'assets/backgrounds/War1/Bright', 'War.png')).convert_alpha()
        self.ennemies = []
        self.player = Player(self.bg_image.get_width() * 0.3,
                             self.bg_image.get_height(), 64, 10, '')
        self.background = Background(self.bg_image)
        self.win = surface
        self.pause = False

    def redrawScene(self):
        self.background.draw(self.win)
        self.player.draw(self.win)

        for ennemy in self.ennemies:
            ennemy.draw(self.win)

        pygame.display.flip()

    def launch(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            self.win.fill((0, 0, 0))
            if self.player.getHealth() <= 0:
                run = False

            if self.player.score >= 100:
                run = False

            keys = pygame.key.get_pressed()
            playerCollided = False

            if len(self.ennemies) <= self.player.score / 10:
                tankX = self.bg_image.get_width() if self.player.direction == pygame.K_RIGHT else 0

                self.ennemies.append(
                    Tank(tankX - randrange(0, 300), self.bg_image.get_height(),
                         64, 0,  pygame.K_RIGHT if tankX != 0 else pygame.K_LEFT))

            for ennemy in self.ennemies:
                if ennemy.x != self.player.x + self.player.width:
                    ennemy.handle_move(
                        keys, self.background.moving_speed)
                # else:
                #     playerCollided = True
                ennemy.draw(self.win)

                for bullet in ennemy.bullets:
                    if bullet.x >= self.player.x and bullet.x <= self.player.x + self.player.width and (bullet.y <= self.player.y + self.player.height and bullet.y + bullet.height >= self.player.y - self.player.height):
                        self.player.takeDamage(bullet.damage, self.win)
                        self.player.health -= 1
                        ennemy.bullets.pop(ennemy.bullets.index(bullet))

                for bullet in self.player.bullets:
                    if ennemy.health > 0:
                        if bullet.x >= ennemy.x and bullet.x <= ennemy.x + ennemy.width and (bullet.y <= ennemy.y + ennemy.height and bullet.y + bullet.height >= ennemy.y - ennemy.height):
                            ennemy.takeDamage(bullet.damage, self.win)
                            self.player.bullets.pop(
                                self.player.bullets.index(bullet))
                        if ennemy.health == 0:
                            ennemy.die(self.win)
                if ennemy.health <= 0 and not ennemy.isExploding:
                    self.ennemies.pop(self.ennemies.index(ennemy))
                    self.player.increaseScore(5)

            self.background.handle_move(
                keys, playerCollided, self.player.direction)

            self.player.handleKeyPress(keys)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

            self.redrawScene()
            clock.tick(60)
