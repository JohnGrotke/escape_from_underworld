import pygame
import json


class Player:
    def __init__(self, x, y, width, height, speed, level):

        with open("configs/player.json", 'r') as file:
            data = json.load(file)

        self.width = data.get('width', 50)
        self.height = data.get('height', 50)
        image_path = data.get('image', 'images/player.png')
        self.image = pygame.transform.scale(pygame.image.load(
            image_path).convert_alpha(), (self.width, self.height))
        self.speed = data.get('speed', 5)
        self.experience = data.get('experience', 0)
        self.next_level_exp = data.get('next_level_exp', 10)
        self.level = data.get('level', 1)
        self.shoot_cooldown = data.get('shoot_cooldown', 10)
        
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def gain_experience(self, exp):
        self.experience = self.experience + exp
        while (self.experience >= self.next_level_exp):
            self.level += 1
            self.experience -= self.next_level_exp
