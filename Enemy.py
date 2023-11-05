import pygame
import random
import json
from Gold_Coin import Gold_Coin
from Blue_Gem import Blue_Gem


class Enemy:
    def __init__(self, screen, config_path, image_path, drop_type, drop_rate, health, exp):
        # Load configuration from the JSON file
        with open(config_path, 'r') as file:
            data = json.load(file)

        self.screen = screen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.alpha = 255

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        # self.image = pygame.transform.scale(
        #     self.image, (self.width, self.height))

        self.speed = data.get('speed')
        self.dx = data.get('dx')
        self.dy = data.get('dy')
        self.drop_rate = drop_rate
        self.drop_type = drop_type
        self.health = health
        self.immunity = False
        self.immunity_frames = 0
        self.exp = exp
        self.knockback_modifier = 1
        self.hit_by = []

        self.x = 0
        self.y = 0

    def move(self, goal_x, goal_y):
        dx = goal_x - self.x
        dy = goal_y - self.y
        dist = ((dx ** 2) + (dy ** 2)) ** 0.5
        if dist > 0:
            dx = dx / dist
            dy = dy / dist
            self.dx = dx * self.speed * self.knockback_modifier
            self.dy = dy * self.speed * self.knockback_modifier
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.knockback_modifier <= 1:
            self.knockback_modifier = self.knockback_modifier + .1

        if self.immunity_frames > 0:
            self.immunity_frames -= 1

        if self.immunity_frames == 0:
            self.immunity = False

    def spawn(self):
        side = random.choice(["top", "left", "right"])
        if side == "top":
            self.x = random.randint(
                0, self.screen.get_width() - self.screen.get_width() // 10)
            self.y = -self.screen.get_height() // 10
        elif side == "left":
            self.x = -self.screen.get_width() // 10
            self.y = random.randint(
                0, self.screen.get_height() - self.screen.get_height() // 10)
        else:  # "right"
            self.x = self.screen.get_width() + self.screen.get_width() // 10
            self.y = random.randint(
                0, self.screen.get_height() - self.screen.get_height() // 10)

        # print(f"spawning new enemy on {side} ({self.x}, {self.y})")

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def hit_killed(self, projectile):
        killed = False
        contact = projectile.id not in self.hit_by

        if contact:
            # if not self.immunity:
                self.health -= projectile.damage
                # self.immunity = True
                # self.immunity_frames = 6
                self.knockback_modifier = -1
                self.hit_by.append(projectile.id)
        
        killed  = self.health <= 0
        
        return (killed, contact)

    def roll_drop(self, drops):
        rand = random.random()
        if rand > self.drop_rate:
            if self.drop_type == "gold_coin":
                drop = Gold_Coin(self.screen, self.x +
                                 self.width / 2, self.y + self.height / 2)
            elif self.drop_type == "blue_gem":
                drop = Blue_Gem(self.screen, self.x +
                                self.width / 2, self.y + self.height / 2)
            drops.append(drop)
