import pygame
import json
from Enemy import Enemy


class Ogre(Enemy):
    def __init__(self, screen):
        config_path = "configs/ogre.json"
        image_path = "images/ogre.png"
        drop_type = "blue_gem"
        drop_rate = .5
        health = 100
        exp = 1
        super().__init__(screen, config_path, image_path, drop_type, drop_rate, health, exp)
