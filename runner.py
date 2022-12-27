import pygame
import sys
import random
import player
import mushroom as shroom
import centipede as centi
 
class Runner():
    def __init__(self, fps=60):
        self.running = True

        self.FPS = fps

        self.speed_increase = 5

        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption("Centipede")

        self.player = player.Player(pos=(self.screen.get_rect().width / 2, self.screen.get_rect().height - 40), fps=self.FPS)

        self.mushrooms = pygame.sprite.Group()
        for i in range(50):
            self.mushrooms.add( shroom.Mushroom((random.randrange(0, self.screen.get_rect().width / 20 - 1) * 20, random.randrange(0, self.screen.get_rect().height / 20 - 1) * 20), (0, 255, 0)) )

        self.centipedes = pygame.sprite.Group()
        self.centipedes.add( centi.Centipede() )

        self.up_limit = self.screen.get_rect().height - 140

        self.clock = pygame.time.Clock()

        

    def update(self):
        self.clock.tick(self.FPS)

        # Inputs
        space = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    space = True
            
        inputs = [0, 0]
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            inputs[0] += 1
        if pressed[pygame.K_LEFT]:
            inputs[0] -= 1
        if pressed[pygame.K_UP]:
            inputs[1] -= 1
        if pressed[pygame.K_DOWN]:
            inputs[1] += 1
        
        self.player.update(self.screen, self.up_limit, inputs, space)
        self.centipedes.update(self.screen)
        

        # Bullet - Mushroom collision
        collided = pygame.sprite.groupcollide(self.player.bullets, self.mushrooms, True, False)
        for bullet in collided.keys():
            for mushroom in collided[bullet]:
                mushroom.take_damage(1)

        # Bullet - Centipede collision
        for cent in self.centipedes:
            collided = pygame.sprite.groupcollide(cent.body, self.player.bullets, False, True)
            for unit in collided.keys():
                for bullet in collided[unit]:
                    if cent.body.sprites().index(unit) == 0:
                        cent.kill()
                    else:
                        length = cent.length
                        index = cent.body.sprites().index(unit)

                        if cent.dir == "RIGHT":
                            c1 = centi.Centipede( length=index, pos=(cent.body.sprites()[len(cent.body.sprites()) - 1].pos[0] - cent.size * index, cent.body.sprites()[len(cent.body.sprites()) - 1].pos[1]), direction=cent.dir)
                            c2 = centi.Centipede( length=length - index - 1, pos=cent.body.sprites()[0].pos, direction=cent.dir)
                        else:
                            c1 = centi.Centipede( length=index, pos=(cent.body.sprites()[len(cent.body.sprites()) - 1].pos[0] - cent.size * index, cent.body.sprites()[len(cent.body.sprites()) - 1].pos[1]), direction=cent.dir)
                            c2 = centi.Centipede( length=length - index - 1, pos=cent.body.sprites()[0].pos, direction=cent.dir)
                        
                        self.mushrooms.add( shroom.Mushroom(unit.pos, color=(0, 255, 0)) )

                        self.centipedes.remove(cent)
                        cent.kill()
                        del(cent)
                        self.centipedes.add(c1)
                        self.centipedes.add(c2)

                        print ( self.centipedes )

        # WORK ON THIS NERD

        # Centipede - Mushroom collision
        for centipede in self.centipedes:
            collided = pygame.sprite.groupcollide(pygame.sprite.Group(centipede.body.sprites()[0]), self.mushrooms, False, False)
            for unit in collided.keys():
                for mushroom in collided[unit]:
                    centipede.collide(self.screen)
        
        # Centipede - Centipede Collision

        # for i in range(len(self.centipedes.sprites()) - 1):
        #     collided = pygame.sprite.groupcollide(pygame.sprite.Group(self.centipedes.sprites()[i].body.sprites[0]), pygame.sprite.Group(self.centipedes.sprites()[i+1].body.sprites[0]), False, False)
        #     for centipede1 in collided.keys():
        #         for centipede2 in collided[centipede1]:
        #             centipede1.collide(self.screen)
        #             centipede2.collide(self.screen)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for centipede in self.centipedes:
            centipede.draw(self.screen)
        self.mushrooms.draw(self.screen)
        pygame.display.update()