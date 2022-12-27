import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, velocity=-3, width=5, height=10, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.v = velocity
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.image = pygame.surface.Surface((width, height))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self):
        self.rect.y += self.v
        self.pos = self.rect.topleft
    
    def draw(self, screen):
        screen.blit(self.image, self.pos)