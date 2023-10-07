import pygame
import math
import json


class Fireball:
    def __init__(self, screen, x, y, direction):

        # Load configuration from the JSON file
        with open("configs/fireball.json", 'r') as file:
            data = json.load(file)

        # Load the image
        image_path = data.get('image_path', 'images/fireball.png')

        # Initialize other attributes from the JSON data
        self.width = data.get('width') / 100 * screen.get_width()
        self.height = data.get('height') / 100 * screen.get_width()
        self.image = pygame.transform.scale(pygame.image.load(
            image_path).convert_alpha(), (self.width, self.height))

        self.screen_normalization = math.sqrt(
            screen.get_width() ** 2 + screen.get_height() ** 2) / 2
        self.speed_percentage = data.get(
            'speed_percentage')/100 * self.screen_normalization

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = direction

    def update(self, screen):
        self.rect.move_ip(self.direction[0], self.direction[1])
        self.x += self.direction[0] * self.speed_percentage
        self.y += self.direction[1] * self.speed_percentage

        # print("x: ", self.x, " y: ", self.y)
        if self.x < 0 or self.x > screen.get_width() or self.y < 0 or self.y > screen.get_height():
            print("Fireball went off screen and was deleted")
            return False  # fireball is off screen and needs to be deleted
        else:
            return True  # fireball is still on screen

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
