import pygame
import json
from Fireball import Fireball


class Player:
    def __init__(self, x, y):

        with open("configs/player.json", 'r') as file:
            data = json.load(file)

        self.width = data.get('width')
        self.height = data.get('height')
        image_path = data.get('image')
        self.image = pygame.transform.scale(pygame.image.load(
            image_path).convert_alpha(), (self.width, self.height))
        self.speed = data.get('speed')
        self.experience = 0
        self.next_level_exp = 10
        self.level = 1
        self.shoot_cooldown = data.get('shoot_cooldown')
        self.weapon_type = data.get('weapon_type')
        
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_level(self, level):
        self.level = level
        self.next_level_exp = self.level * 10

    def set_experience(self, experience):
        self.experience = experience
        self.next_level_exp += self.level * 10

    def gain_experience(self, exp):
        self.experience = self.experience + exp
        while (self.experience >= self.next_level_exp):
            self.experience -= self.next_level_exp
            self.next_level_exp += self.level * 10
            self.level += 1

    def shoot(self, projectiles):
        
        if (self.weapon_type == "fireball"):
            
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculate direction vector between player and mouse cursor
            direction_vector = pygame.math.Vector2(
                mouse_x - self.x, mouse_y - self.y).normalize()

            fireball = Fireball(self.x,
                                self.y,
                                direction_vector)

            projectiles.append(fireball)
            print("Added fireball at {}, {}".format( self.x, self.y))
        else: 
            print("unsupported weapon_type: {}".format(self.weapon_type))
