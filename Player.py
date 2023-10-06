import pygame

class Player:
    def __init__(self, x, y, width, height, speed, level):

        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(
            "images/player.png").convert_alpha(), (width, height))
        self.x = x
        self.y = y
        self.speed = speed
        self.experience = 0
        self.next_level_exp = 10
        self.level = 1
        self.rect = pygame.Rect(x, y, width, height)

    def gain_experience(self, exp):
        self.experience = self.experience + exp
        while (self.experience >= self.next_level_exp):
            self.level += 1
            self.experience -= self.next_level_exp
