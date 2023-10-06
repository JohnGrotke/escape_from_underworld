import pygame
import random
from Fireball import Fireball
from Player import Player
from Enemy import Enemy
from Fallen import Fallen


def check_player_movement(keys):

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed


def update_enemies(m_enemies, player):
    # Move m_enemies towards the player
    for i, enemy in enumerate(m_enemies):
        enemy.move(player.x, player.y)
        enemy.draw(m_screen)
        

        if check_collision(player.x, player.y, player.width, player.height, enemy.x, enemy.y, enemy.width, enemy.height):
            # player and enemy have collided, restart game
            game_over(m_screen, screen_width, screen_height)
            m_enemies = []
            break


def spawn_enemies(m_enemies, spawn_rate):
    # Spawn m_enemies randomly
    if random.random() < spawn_rate:
        enemy = Fallen()
        (enemy_x, enemy_y) = enemy.spawn(m_screen)
        print("spawning new enemy at (", enemy_x, ", ", enemy_y, ")")
        m_enemies.append(enemy)


def check_collision(player_x, player_y, player_width, player_height, enemy_x, enemy_y, enemy_width, enemy_height):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    return player_rect.colliderect(enemy_rect)


def game_over(m_screen, width, height):
    font = pygame.font.Font(None, 36)
    text = font.render(
        "Game Over - Press any key to restart", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    m_screen.blit(text, text_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return


def generate_fallen(m_screen, enemy_width, enemy_height):
    side = random.choice(["top", "left", "right"])
    if side == "top":
        x = random.randint(0, m_screen.get_width() - enemy_width)
        y = random.randint(-enemy_height, -1)
    # elif side == "bottom":
    #     x = random.randint(0, width - enemy_width)
    #     y = random.randint(width-enemy_height, -1)
    elif side == "left":
        x = random.randint(-enemy_width, -1)
        y = random.randint(0, m_screen.get_height() - enemy_height)
    else:  # "right"
        x = random.randint(m_screen.get_width() + 1,
                           m_screen.get_width() + enemy_width)
        y = random.randint(0, m_screen.get_height() - enemy_height)
    return [x, y]


def draw_fireballs(m_fireballs, m_screen):
    for fireball in m_fireballs:
        if (fireball.update(m_screen)):
            fireball.draw(m_screen)
        else:
            m_fireballs.remove(fireball)


def fire(m_fireballs, player):
    fireball_x = player.x + player.width // 2 - fireball_width // 2
    fireball_y = player.y

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate direction vector between player and mouse cursor
    direction_vector = pygame.math.Vector2(
        mouse_x - fireball_x, mouse_y - fireball_y)
    direction_vector.normalize()

    # Multiply direction vector by speed to get velocity vector
    velocity_vector = direction_vector.normalize() * fireball_speed

    fireball = Fireball(fireball_x,
                        fireball_y,
                        velocity_vector)

    m_fireballs.append(fireball)


def check_fireball_collision(m_fireballs, m_enemies):

    for i, fireball in enumerate(m_fireballs):
        for j, enemy in enumerate(m_enemies):
            if check_collision(fireball.x, fireball.y, fireball.width, fireball.height, enemy.x, enemy.y, enemy_width, enemy_height):

                # fireball and enemy have collided, Remove them
                m_enemies.remove(m_enemies[j])
                player.gain_experience(1)
                break


# Initialize pygame
pygame.init()

# Set up the display
screen_width = 640
screen_height = 480

# Load the background image
background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height))

m_screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Escape From Underworld")

enemy_width = 30
enemy_height = 30
enemy_speed = 5
spawn_rate = .02

# Set up the player
player_width = 30
player_height = 30
player_x = screen_width // 2 - player_width // 2
player_y = screen_height // 2 - player_height // 2
player_speed = 5
player = Player(player_x, player_y, player_width,
                player_height, player_speed, 1)

# set up the fireball
fireball_width = 30
fireball_height = 30
fireball_speed = 10
fireball_cooldown = 10
fireball_frames_to_ignore = fireball_cooldown

# Set up the enemy list
m_enemies = []
m_fireballs = []

# Set up the clock
clock = pygame.time.Clock()
fps = 60

# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Draw the background image
    m_screen.blit(background_image, (0, 0))
    # Draw the player
    m_screen.blit(player.image, (player.x, player.y))

    # Draw the HUD
    hud_font = pygame.font.Font(None, 36)
    level_text = hud_font.render(
        "Level: {}".format(player.level), True, (255, 0, 0))

    health_bar_width = screen_width / 2
    pygame.draw.rect(m_screen,
                     "red",
                     (screen_width/4,
                      screen_height/40,
                      int(screen_width/2),
                      screen_height/40))
    pygame.draw.rect(m_screen,
                     "green",
                     (screen_width/4,
                      screen_height/40,
                      int((screen_width/2) *
                          (player.experience / player.next_level_exp)),
                      screen_height/40
                      ))

    m_screen.blit(level_text, (screen_width/20, screen_height/40))

    # Move the player
    keys = pygame.key.get_pressed()
    check_player_movement(keys)

    if keys[pygame.K_SPACE] and fireball_frames_to_ignore == 0:
        fire(m_fireballs, player)
        fireball_frames_to_ignore = fireball_cooldown

    spawn_enemies(m_enemies, spawn_rate)

    update_enemies(m_enemies, player)

    draw_fireballs(m_fireballs, m_screen)

    check_fireball_collision(m_fireballs, m_enemies)

    if fireball_frames_to_ignore > 0:
        fireball_frames_to_ignore -= 1

    # Update the display
    pygame.display.flip()

    # Clear the m_screen
    m_screen.fill((0, 0, 0))

    # Limit the frame rate
    clock.tick(fps)

# Clean up
pygame.quit()
