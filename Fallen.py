import pygame
import json
from Enemy import Enemy
import math


class Fallen(Enemy):
    def __init__(self, screen):

       # Load configuration from the JSON file
        with open("configs/fallen.json", 'r') as file:
            data = json.load(file)

        # Load the image
        image_path = data.get('image_path', 'images/fallen.png')
        
        self.screen = screen
        self.width = data.get('width') / 100 * screen.get_width()
        self.height = data.get('height') / 100 * screen.get_height()
        self.image = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(), (self.width, self.height))

        self.screen_normalization = math.sqrt(
            screen.get_width() ** 2 + screen.get_height() ** 2) / 2
        self.speed_percentage = data.get(
            'speed_percentage') / 100 * self.screen_normalization

        self.dx = data.get('dx')
        self.dy = data.get('dy')

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
