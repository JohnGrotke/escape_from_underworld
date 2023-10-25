from sys import base_prefix
import pygame
import random
from Player import Player
from Enemy import Enemy
from Fallen import Fallen
from Ogre import Ogre
from Fireball import Fireball
from Upgrades import Upgrades
import json
from Button import Button
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

        self.fallen_spawn_rate = data.get('fallen_spawn_rate')
        self.ogre_spawn_rate = data.get('ogre_spawn_rate')

        self.player = Player(self.screen)
        self.upgrades = Upgrades('configs/upgrades.json')
        self.last_player_level = 1
        self.enemies = []
        self.drops = []
        self.fireballs = []
        self.town_home_open = True

        self.clock = pygame.time.Clock()
        self.fps = data.get('fps')

    def initialize_game(self):
        self.player = Player(self.screen)
        self.fireballs = []
        self.enemies = []
        self.drops = []
        self.town_home_open = True

    def reset_game(self):
        self.player = Player(self.screen)
        self.fireballs = []
        self.enemies = []
        self.drops = []
        self.last_player_level = 1
        self.town_home_open = True

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

    def draw_stats(self):
        stats_surface = self.player.print_stats()

        # Position where you want to display the stats (adjust these values as needed).
        x, y = 10, self.screen.get_height() - stats_surface.get_height() - 10

        # Display the stats on the screen.
        self.screen.blit(stats_surface, (x, y))

    def draw_drops(self):
        for drop in self.drops:
            drop.draw()

    def check_drop_collision(self):
        for i, drop in enumerate(self.drops):
            if self.check_collision(self.player, drop):
                self.player.stats_dict["gold_count"] += drop.value
                self.drops.remove(drop)

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
        if random.random() < self.ogre_spawn_rate:
            enemy = Ogre(self.screen)
            enemy.spawn()
            self.enemies.append(enemy)
        elif random.random() < self.fallen_spawn_rate:
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
                        self.player.gain_exp(enemy.exp)
                        enemy.roll_drop(self.drops)
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

            choice_selected = False

            choice_1_name, choice_1 = self.upgrades.random_upgrade()
            choice_2_name, choice_2 = self.upgrades.random_upgrade()
            choice_3_name, choice_3 = self.upgrades.random_upgrade()

            choice_1_button = Button(self.screen, self.screen_width // 2 - 150//2, self.screen_height * 3 // 10 - 70//2, 250, 70, choice_1_name)
            choice_2_button = Button(self.screen, self.screen_width // 2 - 150//2, self.screen_height * 5 // 10 - 70//2, 250, 70, choice_2_name)
            choice_3_button = Button(self.screen, self.screen_width // 2 - 150//2, self.screen_height * 7 // 10 - 70//2, 250, 70, choice_3_name)

            while not choice_selected:
                for event in pygame.event.get():
                    if choice_1_button.draw_button():
                        self.upgrades.apply_upgrade( self.player, choice_1_name)
                        choice_selected = True

                    if choice_2_button.draw_button():
                        self.upgrades.apply_upgrade( self.player, choice_2_name)
                        choice_selected = True

                    if choice_3_button.draw_button():
                        self.upgrades.apply_upgrade( self.player, choice_3_name)
                        choice_selected = True
                pygame.display.flip()


    def display_leave_shop_button(self):

        leave_shop_button = Button(self.screen, self.screen_width // 2 - 150//2, self.screen_height * 9 // 10 - 70//2, 150, 70, "Leave Shop")
        if leave_shop_button.draw_button():
            self.town_home_open = False

    def town_home(self):
        font = pygame.font.Font(None, 36)

        town_text = font.render(
            "Home Town Shop", True, (255, 0, 0))
        town_text_rect = town_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 10))
        self.screen.blit(town_text, town_text_rect)
        
        upgrade_buttons = [
            {
                "text": "Projectile Speed",
                "cost": 100,  # Adjust the cost as needed
                "upgrade_function": self.upgrades.apply_upgrade,
                "upgrade_name": "Projectile Speed",
            },
            {
                "text": "Projectile Size",
                "cost": 200,  # Adjust the cost as needed
                "upgrade_function": self.upgrades.apply_upgrade,
                "upgrade_name": "Projectile Size",
            },
            {
                "text": "Projectile Damage",
                "cost": 300,  # Adjust the cost as needed
                "upgrade_function": self.upgrades.apply_upgrade,
                "upgrade_name": "Projectile Damage",
            },
        ]

        button_x_start = self.screen.get_width() // 2
        button_y_start = self.screen.get_height() // 5
        button_y = 0
        for upgrade_button in upgrade_buttons:
            upgrade_text = f"{upgrade_button['text']} - Cost: {upgrade_button['cost']} gold"
            button_x = button_x_start
            button_y += button_y_start

            button = Button(self.screen, button_x - 350//2, button_y - 70//2, 350, 70, upgrade_text)
            if button.draw_button():
                print("bought: {}".format(upgrade_button["upgrade_name"]))
                if self.player.stats_dict["gold_count"] >= upgrade_button["cost"]:
                    upgrade_button["upgrade_function"](self.player, upgrade_button["upgrade_name"])
                    self.player.stats_dict["gold_count"] -= upgrade_button["cost"]
                else:
                    print("Not enough gold!")
            

        self.display_leave_shop_button()

        # After the town home section, you can add any other logic to continue the game.

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

            self.draw_stats()

            if self.town_home_open:
                self.town_home()
                pygame.display.flip()

            else:

                self.draw_drops()

                self.check_drop_collision()

                self.spawn_enemies()

                self.update_enemies()

                self.handle_shooting(keys)

                self.draw_fireballs()

                self.check_fireball_collision()

                self.check_player_movement(keys)

                self.level_up()

            pygame.display.flip()
            self.screen.fill((0, 0, 0))
