import pygame
from pygame.locals import *
import pygame_menu

from Classes.Scene import Scene


pygame.init()

W, H = 1920, 1080
surface = pygame.display.set_mode((W, H))
pygame.display.set_caption('Robot world saver')

menu = pygame_menu.Menu('Menu',
                        W * 0.6, H * 0.5, theme=pygame_menu.themes.THEME_DARK)

scene = Scene(surface=surface)

menu.add.button('Jouer', scene.launch)
menu.add.button('Quitter', pygame_menu.events.EXIT)

print(scene.player.score)
menu.mainloop(surface)
