from sys import base_prefix
import pygame
import random
from Player import Player
from Enemy import Enemy
from Fallen import Fallen
from Fireball import Fireball
from Upgrades import Upgrades
import json
import time


class Game:
    def __init__(self):
        pygame.init()

        # Load configuration from the JSON file
        with open("configs/game.json", 'r') as file:
            data = json.load(file)

        self.screen_width = data.get('screen_width')
        self.screen_height = data.get('screen_height')
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption(data.get('title'))

        self.background_image = pygame.image.load(data.get('background_image'))
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen_width, self.screen_height))

        self.spawn_rate = data.get('enemy_spawn_rate')

        self.player = Player(self.screen)
        self.upgrades = Upgrades()
        self.last_player_level = 1

        self.clock = pygame.time.Clock()
        self.fps = data.get('fps')

    def initialize_game(self):
        self.player = Player(self.screen)
        self.fireballs = []
        self.enemies = []

    def reset_game(self):
        self.player = Player(self.screen)
        self.fireballs = []
        self.enemies = []
        self.last_player_level = 1

    def game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render(
            "Game Over - Press any key to restart", True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.reset_game()
                    return

    def draw_background(self):

        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.player.image, (self.player.x, self.player.y))

    def draw_hud(self):
        hud_font = pygame.font.Font(None, 36)
        level_text = hud_font.render("Level: {}, {}/{}".format(self.player.level,
                                     self.player.exp, self.player.next_level_exp), True, (255, 0, 0))

        bar_x = self.screen_width / 4
        bar_y = self.screen_height / 40
        bar_width = self.screen_width / 2
        bar_height = self.screen_height // 40
        bar_percentage = (self.screen_width / 2) * \
            (self.player.exp / self.player.next_level_exp)

        pygame.draw.rect(self.screen,
                         "red",
                         (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen,
                         "green",
                         (bar_x, bar_y, bar_percentage, bar_height))

        self.screen.blit(
            level_text, (self.screen_width / 20, self.screen_height / 40))

    def check_player_movement(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move_up()
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move_down()

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.player.x, self.player.y)
            enemy.draw()

            if self.check_collision(self.player, enemy):
                self.game_over()
                self.enemies = []
                break

    def spawn_enemies(self):
        if random.random() < self.spawn_rate:
            enemy = Fallen(self.screen)
            enemy.spawn()
            self.enemies.append(enemy)

    def check_collision(self, obj_1, obj_2):
        obj_1_rect = pygame.Rect(obj_1.x, obj_1.y, obj_1.width, obj_1.height)
        obj_2_rect = pygame.Rect(obj_2.x, obj_2.y, obj_2.width, obj_2.height)
        return obj_1_rect.colliderect(obj_2_rect)

    def draw_fireballs(self):
        for fireball in self.fireballs:
            if fireball.update(self.screen):
                fireball.draw(self.screen)
            else:
                self.fireballs.remove(fireball)

    def check_fireball_collision(self):
        for i, fireball in enumerate(self.fireballs):
            for j, enemy in enumerate(self.enemies):
                if self.check_collision(fireball, enemy):
                    if enemy.hit_killed(fireball):
                        self.enemies.remove(enemy)
                        self.player.gain_exp(1)
                    else:
                        enemy.immunity = True
                    if not fireball.pierce():
                        self.fireballs.remove(fireball)

                    break

    def handle_shooting(self, keys):
        # Add to the counter each frame even if we didn't shoot
        self.player.frames_since_last_shot += 1

        if keys[pygame.K_SPACE]:
            self.player.shoot(self.fireballs)

    def level_up(self):

        if self.last_player_level < self.player.level:
            self.last_player_level += 1
            font = pygame.font.Font(None, 36)
            text = font.render(
                "LEVEL UP", True, (255, 0, 0))
            text_rect = text.get_rect(
                center=(self.screen_width // 2, self.screen_height / 40))

            option_1_x = self.screen_width / 4
            option_1_y = self.screen_height / 10
            option_1_width = self.screen_width / 2
            option_1_height = self.screen_height // 5

            pygame.draw.rect(self.screen,
                             "red",
                             (option_1_x, option_1_y, option_1_width, option_1_height))
            choice_1 = self.upgrades.random_upgrade()
            choice_2 = self.upgrades.random_upgrade()
            choice_3 = self.upgrades.random_upgrade()

            option_1_text = font.render(choice_1.get(
                "upgrade_text"), True, (255, 255, 255))
            option_1_text_x = option_1_x + option_1_width // 2 - option_1_text.get_width() // 2
            option_1_text_y = option_1_y + option_1_height // 2 - \
                option_1_text.get_height() // 2

            self.screen.blit(option_1_text, (option_1_text_x, option_1_text_y))

            option_2_x = self.screen_width / 4
            option_2_y = 4 * self.screen_height / 10
            option_2_width = self.screen_width / 2
            option_2_height = self.screen_height // 5

            pygame.draw.rect(self.screen,
                             "red",
                             (option_2_x, option_2_y, option_2_width, option_2_height))

            option_2_text = font.render(choice_2.get(
                "upgrade_text"), True, (255, 255, 255))
            option_2_text_x = option_2_x + option_2_width // 2 - option_2_text.get_width() // 2
            option_2_text_y = option_2_y + option_2_height // 2 - \
                option_2_text.get_height() // 2

            self.screen.blit(option_2_text, (option_2_text_x, option_2_text_y))

            option_3_x = self.screen_width / 4
            option_3_y = 7 * self.screen_height / 10
            option_3_width = self.screen_width / 2
            option_3_height = self.screen_height // 5

            pygame.draw.rect(self.screen,
                             "red",
                             (option_3_x, option_3_y, option_3_width, option_3_height))

            option_3_text = font.render(choice_3.get(
                "upgrade_text"), True, (255, 255, 255))
            option_3_text_x = option_3_x + option_3_width // 2 - option_3_text.get_width() // 2
            option_3_text_y = option_3_y + option_3_height // 2 - \
                option_3_text.get_height() // 2

            self.screen.blit(option_3_text, (option_3_text_x, option_3_text_y))

            self.screen.blit(text, text_rect)
            pygame.display.update()

            choice_1_selected = False
            choice_2_selected = False
            choice_3_selected = False
            choice_selected = False

            while not choice_selected:
                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        choice_selected = True
                        self.reset_game()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        choice_1_selected = option_1_x <= event.pos[0] <= option_1_x + \
                            option_1_width and option_1_y <= event.pos[1] <= option_1_y + \
                            option_1_height
                        choice_2_selected = option_2_x <= event.pos[0] <= option_2_x + \
                            option_2_width and option_2_y <= event.pos[1] <= option_2_y + \
                            option_2_height
                        choice_3_selected = option_3_x <= event.pos[0] <= option_2_x + \
                            option_3_width and option_3_y <= event.pos[1] <= option_3_y + \
                            option_3_height

                        if (choice_1_selected or choice_2_selected or choice_3_selected):
                            if choice_1_selected:
                                self.upgrades.apply_upgrade(
                                    self.player, choice_1)
                            elif choice_2_selected:
                                self.upgrades.apply_upgrade(
                                    self.player, choice_2)
                            else:
                                self.upgrades.apply_upgrade(
                                    self.player, choice_3)

                            choice_selected = True

    def run_game(self):
        self.initialize_game()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys = pygame.key.get_pressed()

            self.draw_background()

            self.draw_hud()

            self.spawn_enemies()

            self.update_enemies()

            self.handle_shooting(keys)

            self.draw_fireballs()

            self.check_fireball_collision()

            self.check_player_movement(keys)

            self.level_up()

            pygame.display.flip()
            self.screen.fill((0, 0, 0))
