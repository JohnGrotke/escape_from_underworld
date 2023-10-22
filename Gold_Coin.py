import pygame
from Drop import Drop


class Gold_Coin(Drop):
    def __init__(self, screen, x, y):
        image_path = "images/gold_coin.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.x = x
        self.y = y
        self.screen = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.value = 1
