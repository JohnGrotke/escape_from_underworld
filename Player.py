import pygame
import json
import math
from Fireball import Fireball


class Player:
    def __init__(self, screen):

        with open("configs/player.json", 'r') as file:
            data = json.load(file)

        self.screen = screen

        image_path = data.get('image')
        self.image = pygame.image.load(image_path)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.fliq_image = 0

        self.screen_normalization = math.sqrt(
            screen.get_width() ** 2 + screen.get_height() ** 2) / 2
        self.frames_since_last_shot = 0

        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.exp = 0
        self.next_level_exp = 10
        self.level = 1

        self.stats_dict = {
            "width": self.width,
            "height": self.height,
            "speed": data.get('speed') / 100 * self.screen_normalization,
            "shoot_cooldown": data.get('shoot_cooldown'),
            "weapon_type": data.get('weapon_type'),
            "projectile_speed": data.get('projectile_speed'),
            "projectile_size": data.get('projectile_size'),
            "projectile_damage": data.get('projectile_damage'),
            "projectile_piercing": data.get('projectile_piercing'),
            "health": data.get('health'),
            "direction": "left",
            "gold_count": 1000
        }

    def set_level(self, level):
        self.level = level
        self.next_level_exp = self.level * 10

    def set_exp(self, exp):
        self.exp = exp

    def gain_exp(self, exp):
        self.exp = self.exp + exp
        while (self.exp >= self.next_level_exp):
            self.exp -= self.next_level_exp
            self.next_level_exp += self.level * 10
            self.level += 1

    def shoot(self, projectiles):
        if (self.stats_dict.get("weapon_type") == "fireball"):
            if (self.frames_since_last_shot > self.stats_dict["shoot_cooldown"]):
                self.frames_since_last_shot = 0
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate direction vector between player and mouse cursor
                direction_vector = pygame.math.Vector2(
                    mouse_x - self.x, mouse_y - self.y).normalize()

                fireball = Fireball(self.screen,
                                    self.x,
                                    self.y,
                                    direction_vector,
                                    self.stats_dict.get("projectile_speed"),
                                    self.stats_dict.get("projectile_size"),
                                    self.stats_dict.get("projectile_damage"),
                                    self.stats_dict.get("projectile_piercing"))

                projectiles.append(fireball)
                # print("Added fireball at {}, {}".format(self.x, self.y))
            else:
                pass
                # print("tried adding a fireball but hasn't been long enough {} < {}".format(self.frames_since_last_shot, self.shoot_cooldown))

        else:
            print("unsupported weapon_type: {}".format(self.weapon_type))

    def move_left(self):
        self.x -= self.stats_dict["speed"]
        if self.stats_dict["direction"] == "right":
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.stats_dict["direction"] = "left"

    def move_right(self):
        self.x += self.stats_dict["speed"]
        if self.stats_dict["direction"] == "left":
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.stats_dict["direction"] = "right"

    def move_down(self):
        self.y += self.stats_dict["speed"]

    def move_up(self):
        self.y -= self.stats_dict["speed"]

    def print_stats(self):
        # Create a list of strings with formatted information from the stats_dict.
        pretty_text = [f"{key}: {value:.2f}" if isinstance(
            value, float) else f"{key}: {value}" for key, value in self.stats_dict.items()]

        # Create a Pygame font for rendering text.
        # You can choose a smaller font size if needed.
        font = pygame.font.Font(None, 24)

        # Create a Pygame surface with a transparent background.
        line_height = 24  # Adjust this value based on your font size.
        text_surface = pygame.Surface(
            (400, line_height * len(pretty_text)), pygame.SRCALPHA)

        for i, line in enumerate(pretty_text):
            # White text color.
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.topleft = (0, i * line_height)
            text_surface.blit(text, text_rect)

        return text_surface
