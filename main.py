import pygame
import runner

pygame.init()

runner = runner.Runner()
while runner.running:
    runner.update()
    runner.draw()