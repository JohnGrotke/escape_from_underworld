import pygame
import random


class Enemy:
    def __init__(self, x, y, width, height, speed):

        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(
            'images/fallen.png').convert_alpha(), (self.width, self.height))
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, goal_x, goal_y):
        dx = goal_x - self.x
        dy = goal_y - self.y
        dist = ((dx ** 2) + (dy ** 2)) ** 0.5
        if dist > 0:
            dx = dx / dist
            dy = dy / dist
            self.dx = dx * self.speed
            self.dy = dy * self.speed
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def spawn(self, screen):
        side = random.choice(["top", "left", "right"])
        if side == "top":
            x = random.randint(0, screen.get_width() - screen.get_width()/10)
            y = -screen.get_height()//10
        elif side == "left":
            x = -screen.get_width()//10
            y = random.randint(0, screen.get_height() -
                               screen.get_height()//10)
        else:  # "right"
            x = screen.get_width() + screen.get_width()//10
            y = random.randint(0, screen.get_height() -
                               screen.get_height()//10)

        print("spawning new enemy at on ", side, "(", x, ", ", y, ")")
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
