import pygame

class Drop:
    def __init__(self, screen, x, y, image_path, value):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.x = x
        self.y = y
        self.screen = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.value = value

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
