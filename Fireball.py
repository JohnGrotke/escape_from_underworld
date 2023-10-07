import pygame
import json


class Fireball:
    def __init__(self, x, y, direction):

        # Load configuration from the JSON file
        with open("configs/fireball.json", 'r') as file:
            data = json.load(file)

        # Load the image
        image_path = data.get('image_path', 'images/fireball.png')
        self.image = pygame.transform.scale(pygame.image.load(
            image_path).convert_alpha(), (data.get('width'), data.get('height')))

        # Initialize other attributes from the JSON data
        self.width = data.get('width')
        self.height = data.get('height')
        self.speed = data.get('speed')

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = direction

    def update(self, screen):
        self.rect.move_ip(self.direction[0], self.direction[1])
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # print("x: ", self.x, " y: ", self.y)
        if self.x < 0 or self.x > screen.get_width() or self.y < 0 or self.y > screen.get_height():
            print("Fireball went off screen and was deleted")
            return False  # fireball is off screen and needs to be deleted
        else:
            return True  # fireball is still on screen

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
