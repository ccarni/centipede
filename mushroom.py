import pygame
import math

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, pos, color=(0, 255, 0), health=2, width=20, height=20):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.color = color
        self.pos = pos
        self.width = width
        self.height = height

        self.image = pygame.surface.Surface((width, height))
        rect = self.image.get_rect()
        
        pygame.draw.arc(self.image, self.color, rect, 0, math.pi)
        pygame.draw.line(self.image, self.color, ((rect.left) , (rect.top / 2 + self.height / 2)), ((rect.right) , (rect.top / 2 + self.height / 2)))
        pygame.draw.rect(self.image, self.color, pygame.rect.Rect(rect.left + (self.width / 4), rect.top + (self.height / 2), self.width / 2, self.height / 2))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()