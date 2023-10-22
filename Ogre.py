import pygame
import json
from Enemy import Enemy
from Blue_Gem import Blue_Gem
import math


class Ogre(Enemy):
    def __init__(self, screen):

       # Load configuration from the JSON file
        with open("configs/ogre.json", 'r') as file:
            data = json.load(file)

        # Load the image
        image_path = data.get('image_path')

        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = self.image.convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.speed = data.get('speed')

        self.dx = data.get('dx')
        self.dy = data.get('dy')
        self.exp = data.get('exp')
        self.drop_rate = .5
        self.drop_type = "blue_gem"

        self.health = 100
        self.immunity = False
        self.immunity_frames = 0

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)