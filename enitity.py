import pygame

class Entity(pygame.Spirte.sprite):
    def __init__(self, x, y, groups: pygame.sprite.Group):
        super.__init__(groups)
        self.x = x
        self.y = y 