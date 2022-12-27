import pygame

class Unit(pygame.sprite.Sprite):
    def __init__(self, size, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.skin = pygame.Surface((size, size))
        self.skin.fill(color)

        self.pos = pos
        self.rect = self.skin.get_rect()
        self.rect.topleft = pos
    
    def update(self):
        self.rect.topleft = self.pos
    
    def draw(self, screen):
        screen.blit(self.skin, self.pos)

class Centipede(pygame.sprite.Sprite):
    def __init__(self, size=20, length=20, color=(0, 255, 0), pos=(0,0), direction="RIGHT"):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.length = length
        self.color = color
        self.pos = pos
        self.dir = direction
        
        self.body = pygame.sprite.Group()

        # Create the body
        for i in range(self.length):
            if self.dir == "RIGHT":
                self.body.add(Unit(self.size, self.color, (self.pos[0] - self.size*i, self.pos[1])))
            elif self.dir == "LEFT":
                self.body.add(Unit(self.size, self.color, (self.pos[0] + self.size*i, self.pos[1])))
            elif self.dir == "UP":
                self.body.add(Unit(self.size, self.color, (self.pos[0], self.pos[1] + self.size*i)))
            elif self.dir == "DOWN":
                self.body.add(Unit(self.size, self.color, (self.pos[0], self.pos[1] - self.size*i)))

    def de_update(self, screen):
        # Update the rest of the body
        for i in range(len(self.body.sprites()) - 1):
            self.body.sprites()[i].pos = self.body.sprites()[i + 1].pos
        
        # Update the head
        end = len(self.body.sprites()) - 1
        if self.dir == "RIGHT":
            self.body.sprites()[end].pos = (self.body.sprites()[end].pos[0] - self.size, self.body.sprites()[end].pos[1])
        elif self.dir == "LEFT":
            self.body.sprites()[end].pos = (self.body.sprites()[end].pos[0] + self.size, self.body.sprites()[end].pos[1])
        elif self.dir == "UP":
            self.body.sprites()[end].pos = (self.body.sprites()[end].pos[0], self.body.sprites()[end].pos[1] + self.size)
        elif self.dir == "DOWN":
            self.body.sprites()[end].pos = (self.body.sprites()[end].pos[0], self.body.sprites()[end].pos[1] - self.size)
    
    def update(self, screen):
        self.body.update()

        # Update the rest of the body
        for i in range(len(self.body.sprites()) - 1, 0, -1):
            self.body.sprites()[i].pos = self.body.sprites()[i - 1].pos
        
        # Update the head
        if self.dir == "RIGHT":
            self.body.sprites()[0].pos = (self.body.sprites()[0].pos[0] + self.size, self.body.sprites()[0].pos[1])
        elif self.dir == "LEFT":
            self.body.sprites()[0].pos = (self.body.sprites()[0].pos[0] - self.size, self.body.sprites()[0].pos[1])
        elif self.dir == "UP":
            self.body.sprites()[0].pos = (self.body.sprites()[0].pos[0], self.body.sprites()[0].pos[1] - self.size)
        elif self.dir == "DOWN":
            self.body.sprites()[0].pos = (self.body.sprites()[0].pos[0], self.body.sprites()[0].pos[1] + self.size)
        
        # Handle collisions
        if (self.body.sprites()[0].pos[0] >= screen.get_rect().width) or (self.body.sprites()[0].pos[0] < 0):
            self.collide(screen)

    def collide(self, screen):
        original_dir = self.dir

        self.de_update(screen)
        self.dir = "DOWN"
        self.update(screen)

        if original_dir == "RIGHT":
            self.dir = "LEFT"
        else:
            self.dir = "RIGHT"
        


    def draw(self, screen):
        for unit in self.body:
            unit.draw(screen)