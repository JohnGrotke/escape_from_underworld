import pygame
from Enemy import Enemy


class Fallen(Enemy):
    def __init__(self, x, y, width, height, speed):

        self.image = pygame.transform.scale(pygame.image.load(
            'images/fallen.png').convert_alpha(), (30, 30))
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.rect = pygame.Rect(x, y, width, height)
