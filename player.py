import pygame
import bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, width=20, height=20, color = (251, 206, 177), pos=[0, 0], speed=240, fps=60):
        pygame.sprite.Sprite.__init__(self)
        self.height = height
        self.color = color
        self.speed = speed/fps
        self.FPS = fps

        self.image = pygame.surface.Surface((width, height))
        self.image.fill(color)

        self.pos = list(pos)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.v = [0,0]

        self.bullets = pygame.sprite.Group()
    
    def update(self, screen, up_limit, inputs=[0, 0], space=False):
        self.v = [inputs[0] * self.speed, inputs[1] * self.speed]

        self.rect.x += self.v[0]
        self.rect.y += self.v[1]
    
        self.pos = self.rect.topleft

        if space:
            self.bullets.add(bullet.Bullet(self.pos, velocity=-720/self.FPS))
        
        self.bullets.update()

        # Check bounds
        if self.rect.right > screen.get_rect().right:
            self.rect.right = screen.get_rect().right
        if self.rect.left < screen.get_rect().left:
            self.rect.left = screen.get_rect().left
        if self.rect.bottom > screen.get_rect().bottom:
            self.rect.bottom = screen.get_rect().bottom
        if self.rect.top < up_limit:
            self.rect.top = up_limit

    def draw(self, screen):
        self.bullets.draw(screen)
        screen.blit(self.image, self.pos)