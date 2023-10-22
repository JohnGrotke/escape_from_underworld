import pygame
import json
from Enemy import Enemy


class Fallen(Enemy):
    def __init__(self, screen):
        config_path = "configs/fallen.json"
        image_path = "images/goblin.png"
        drop_type = "gold_coin"
        drop_rate = .5
        health = 10
        exp = 1
        super().__init__(screen, config_path, image_path, drop_type, drop_rate, health, exp)
