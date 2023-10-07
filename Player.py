import pygame
import json
import math
from Fireball import Fireball


class Player:
    def __init__(self, screen):

        with open("configs/player.json", 'r') as file:
            data = json.load(file)

        self.screen = screen
        self.width = data.get('width') / 100 * screen.get_width()
        self.height = data.get('height') / 100 * screen.get_height()
        image_path = data.get('image')
        self.image = pygame.transform.scale(pygame.image.load(
            image_path).convert_alpha(), (self.width, self.height))

        self.screen_normalization = math.sqrt(
            screen.get_width() ** 2 + screen.get_height() ** 2) / 2
        self.speed_percentage = data.get(
            'speed_percentage') / 100 * self.screen_normalization
        self.experience = 0
        self.next_level_exp = 10
        self.level = 1
        self.shoot_cooldown = data.get('shoot_cooldown')
        self.frames_since_last_shot = 0
        self.weapon_type = data.get('weapon_type')

        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_level(self, level):
        self.level = level
        self.next_level_exp = self.level * 10

    def set_experience(self, experience):
        self.experience = experience

    def gain_experience(self, exp):
        self.experience = self.experience + exp
        while (self.experience >= self.next_level_exp):
            self.experience -= self.next_level_exp
            self.next_level_exp += self.level * 10
            self.level += 1

    def shoot(self, projectiles):

        if (self.weapon_type == "fireball"):
            if (self.frames_since_last_shot > self.shoot_cooldown):
                self.frames_since_last_shot = 0
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate direction vector between player and mouse cursor
                direction_vector = pygame.math.Vector2(
                    mouse_x - self.x, mouse_y - self.y).normalize()

                fireball = Fireball(self.screen,
                                    self.x,
                                    self.y,
                                    direction_vector)

                projectiles.append(fireball)
                print("Added fireball at {}, {}".format(self.x, self.y))
            else:
                pass
                # print("tried adding a fireball but hasn't been long enough {} < {}".format(self.frames_since_last_shot, self.shoot_cooldown))

        else:
            print("unsupported weapon_type: {}".format(self.weapon_type))

    def move_left(self):
        self.x -= self.speed_percentage

    def move_right(self):
        self.x += self.speed_percentage

    def move_down(self):
        self.y += self.speed_percentage

    def move_up(self):
        self.y -= self.speed_percentage
