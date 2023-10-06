import pygame

class Fireball:
    def __init__(self, x, y, width, height, speed, direction):

        self.image = pygame.transform.scale(pygame.image.load(
            'images/fireball.png').convert_alpha(), (width, height))
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)

        self.direction = direction

    def update(self, screen):
        self.rect.move_ip(self.direction[0], self.direction[1])
        self.x += self.direction[0]
        self.y += self.direction[1]

        # print("x: ", self.x, " y: ", self.y)
        if self.x < 0 or self.x > screen.get_width() or self.y < 0 or self.y > screen.get_height():
            return False  # fireball is off screen and needs to be deleted
        else:
            return True  # fireball is still on screen

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
