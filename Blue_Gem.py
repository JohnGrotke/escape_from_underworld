import pygame
from Drop import Drop

class Blue_Gem(Drop):
    def __init__(self, screen, x, y):
        image_path = "images/blue_gem.png"
        value = 5
        super().__init__(screen, x, y, image_path, value)
