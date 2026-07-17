import pygame
from globals import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, topleft, surf_or_size, groups):
        super().__init__(groups)
        if isinstance(surf_or_size, pygame.Surface):
            self.image = surf_or_size
            self.rect = self.image.get_frect(topleft=(int(topleft[0]), int(topleft[1])))
        else:
            w, h = map(int, surf_or_size)
            self.image = pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
            self.rect = self.image.get_frect(topleft=(int(topleft[0]), int(topleft[1])))

class MaterialSprite(pygame.sprite.Sprite):
    def __init__(self, topleft, surf_or_size, groups):
        super().__init__(groups)
        if isinstance(surf_or_size, pygame.Surface):
            self.image = surf_or_size
            self.rect = self.image.get_frect(topleft=(int(topleft[0]), int(topleft[1])))
        else:
            w, h = map(int, surf_or_size)
            self.image = pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
            self.rect = self.image.get_frect(topleft=(int(topleft[0]), int(topleft[1])))
        

    def drawMessageBox(self, targetSurface, loadedMessageBox, playerRect):
        print('drawMessage FUNC called')
        print('targetSurface : ', targetSurface)
        print('loadedMessageBox : ', loadedMessageBox)

        target_pos = playerRect
        offset = pygame.Vector2()

        offset.x = -(target_pos[0] - BASEWIDTH / 2)
        offset.y = -(target_pos[1] - BASEHEIGHT / 2)
        
        otherOffset = pygame.Vector2()
        otherOffset.x = -50
        otherOffset.y = -50

        coords = (self.rect.x + offset.x + otherOffset.x, self.rect.y + offset.y + otherOffset.y)

        

        targetSurface.blit(loadedMessageBox, coords)