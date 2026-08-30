import pygame
pygame.init()

pygame.display.set_caption('test')
pygame.screen = pygame.display.set_mode((400, 400))
running = True
while running:

    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False

    