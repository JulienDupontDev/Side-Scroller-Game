import pygame

from Classes.LifeBar import LifeBar


class Character(object):
    def __init__(self, health, attack, defense, x, y, characterDimensions):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.x = x
        self.y = y
        self.lifeBar = LifeBar(
            x, y - 20, characterDimensions[0] * 2.6, self.health)

    def getHealth(self):
        return self.health

    def getAttack(self):
        return self.attack

    def getDefense(self):
        return self.defense

    def setHealth(self, health):
        self.health = health

    # take damage based on defense and subtract from health
    def takeDamage(self, damage, win):
        self.health -= damage
        if self.health < 0:
            self.health = 0

        self.lifeBar.update(win, self.x, self.y, self.health)

    def attackOther(self, target, win):
        damage = self.attack * target.defense
        if damage < 0:
            damage = 0
        target.takeDamage(damage, win)
        return target.getHealth()

    def rotate(surface, direction):
        if(direction == pygame.K_LEFT):
            return pygame.transform.flip(surface, True, False)
        else:
            return surface

    # redimensionne la surface à la taille voulue
    def scale(surface: pygame.Surface, scaleValue: float):
        return pygame.transform.scale(surface, (surface.get_width() * scaleValue, surface.get_height() * scaleValue))
