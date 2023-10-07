import pygame
import json
from Enemy import Enemy


class Fallen(Enemy):
    def __init__(self):

        # Load configuration from the JSON file
        with open("configs/fallen.json", 'r') as file:
            data = json.load(file)

        # Load the image
        image_path = data.get('image_path', 'images/fallen.png')
        self.image = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(), (30, 30))

        # Initialize other attributes from the JSON data
        self.width = data.get('width')
        self.height = data.get('height')
        self.speed = data.get('speed')
        self.dx = data.get('dx')
        self.dy = data.get('dy')

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
