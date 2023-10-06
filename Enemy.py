import pygame
import random

class Enemy:
    def __init__(self, x, y, width, height, speed):

        self.image = pygame.transform.scale(pygame.image.load(
            'images/fallen.png').convert_alpha(), (30, 30))
        self.width = width
        self.height = height
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
            enemy_speed = min(dist, 2)
            self.dx = dx * enemy_speed
            self.dy = dy * enemy_speed
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def spawn(self, screen):
        side = random.choice(["top", "left", "right"])
        if side == "top":
            self.x = random.randint(0, screen.get_width() - self.width)
            self.y = random.randint(-self.height, -1)
        # elif side == "bottom":
        #     x = random.randint(0, width - self.width)
        #     y = random.randint(width-self.height, -1)
        elif side == "left":
            self.x = random.randint(-self.width, -1)
            self.y = random.randint(0, screen.get_height() - self.height)
        else:  # "right"
            self.x = random.randint(screen.get_width() + 1,
                            screen.get_width() + self.width)
            self.y = random.randint(0, screen.get_height() - self.height)
        return [self.x, self.y]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))