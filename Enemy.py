import pygame
import random
import math
import json


class Enemy:
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
        self.immunity_frames = 0
        self.immunity = False

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, goal_x, goal_y):
        dx = goal_x - self.x
        dy = goal_y - self.y
        dist = ((dx ** 2) + (dy ** 2)) ** 0.5
        if dist > 0:
            dx = dx / dist
            dy = dy / dist
            self.dx = dx * self.speed_percentage
            self.dy = dy * self.speed_percentage
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        # Set immunity on movement
        if self.immunity_frames > 0:
            self.immunity_frames -= 1

        if self.immunity_frames == 0:
            self.immunity = False

    def spawn(self):
        side = random.choice(["top", "left", "right"])
        if side == "top":
            self.x = random.randint(
                0, self.screen.get_width() - self.screen.get_width()/10)
            self.y = -self.screen.get_height()//10
        elif side == "left":
            self.x = -self.screen.get_width()//10
            self.y = random.randint(0, self.screen.get_height() -
                                    self.screen.get_height()//10)
        else:  # "right"
            self.x = self.screen.get_width() + self.screen.get_width()//10
            self.y = random.randint(0, self.screen.get_height() -
                                    self.screen.get_height()//10)

        print("spawning new enemy at on ", side,
              "(", self.x, ", ", self.y, ")")

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
