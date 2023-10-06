import pygame

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
