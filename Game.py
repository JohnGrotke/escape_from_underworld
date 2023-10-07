import pygame
import random
from Player import Player
from Enemy import Enemy
from Fallen import Fallen
from Fireball import Fireball
import json

class Game:
    def __init__(self):
        pygame.init()

        # Load configuration from the JSON file
        with open("configs/game.json", 'r') as file:
            data = json.load(file)

        self.screen_width = data.get('screen_width')
        self.screen_height = data.get('screen_height')
        self.m_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(data.get('title'))

        self.background_image = pygame.image.load(data.get('background_image'))
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.spawn_rate = data.get('enemy_spawn_rate')

        self.player = Player(self.screen_width // 2, self.screen_height // 2 )

        self.fireball_frames_to_ignore = self.player.shoot_cooldown

        self.clock = pygame.time.Clock()
        self.fps = data.get('fps')

    def initialize_game(self):
        self.player = Player(self.screen_width // 2, self.screen_height // 2 )
        self.fireballs = []
        self.enemies = []

    def reset_game(self):
        self.player = Player(self.screen_width // 2, self.screen_height // 2 )
        self.fireballs = []
        self.enemies = []  

    def check_player_movement(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.player.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.player.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player.speed

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.player.x, self.player.y)
            enemy.draw(self.m_screen)

            if self.check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                                    enemy.x, enemy.y, enemy.width, enemy.height):
                self.game_over()
                self.enemies = []
                break

    def spawn_enemies(self):
        if random.random() < self.spawn_rate:
            enemy = Fallen()
            enemy.spawn(self.m_screen)
            self.enemies.append(enemy)

    def check_collision(self, player_x, player_y, player_width, player_height, enemy_x, enemy_y, enemy_width, enemy_height):
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        return player_rect.colliderect(enemy_rect)

    def game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over - Press any key to restart", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.m_screen.blit(text, text_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.reset_game()
                    return 

    def draw_fireballs(self):
        for fireball in self.fireballs:
            if fireball.update(self.m_screen):
                fireball.draw(self.m_screen)
            else:
                self.fireballs.remove(fireball)

    def check_fireball_collision(self):
        for i, fireball in enumerate(self.fireballs):
            for j, enemy in enumerate(self.enemies):
                if self.check_collision(fireball.x, fireball.y, fireball.width, fireball.height,
                                        enemy.x, enemy.y, enemy.width, enemy.height):
                    self.enemies.remove(self.enemies[j])
                    self.player.gain_experience(1)
                    break

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

            self.m_screen.blit(self.background_image, (0, 0))
            self.m_screen.blit(self.player.image, (self.player.x, self.player.y))

            hud_font = pygame.font.Font(None, 36)
            level_text = hud_font.render("Level: {}, {}/{}".format(self.player.level, self.player.experience, self.player.next_level_exp), True, (255, 0, 0))

            pygame.draw.rect(self.m_screen,
                             "red",
                             (self.screen_width / 4,
                              self.screen_height / 40,
                              int(self.screen_width / 2),
                              self.screen_height / 40))
            pygame.draw.rect(self.m_screen,
                             "green",
                             (self.screen_width / 4,
                              self.screen_height / 40,
                              int((self.screen_width / 2) *
                                  (self.player.experience / self.player.next_level_exp)),
                              self.screen_height / 40
                              ))

            self.m_screen.blit(level_text, (self.screen_width / 20, self.screen_height / 40))

            keys = pygame.key.get_pressed()
            self.check_player_movement(keys)

            if keys[pygame.K_SPACE] and self.fireball_frames_to_ignore == 0:
                self.player.shoot(self.fireballs)
                self.fireball_frames_to_ignore = self.player.shoot_cooldown

            self.spawn_enemies()

            self.update_enemies()

            self.draw_fireballs()

            self.check_fireball_collision()

            if self.fireball_frames_to_ignore > 0:
                self.fireball_frames_to_ignore -= 1

            pygame.display.flip()
            self.m_screen.fill((0, 0, 0))
