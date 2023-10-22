import pygame
from Drop import Drop


class Gold_Coin(Drop):
    def __init__(self, screen, x, y):
        image_path = "images/gold_coin.png"
        value = 1
        super().__init__(screen, x, y, image_path, value)
