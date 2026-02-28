import pygame
from entity import Entity
from mouse import Mouse




class User(Entity):

    def __init__(self, x: int, y: int, groups: pygame.sprite.Group):
        super().__init__(x, y, groups)

        self.mouse = Mouse(pygame.mouse)
        self.pos = pygame.math.Vector2(x, y)
        self.image
        self.basic = 'hello world'
        self.mousePositions = ()

    def printPosition(self):
        print(self.pos)

    def getUpdateReturnMousePos(self):
        mousePos = self.mouse.getUpdateMousePos()
        return mousePos
    
    def movePlayer(self, mousePos):
        self.pos = pygame.math.Vector2(mousePos[0], mousePos[1])
        print('self.pos : ', self.pos)


    def moveToMouse(self):
        #first step is to get the mouse coords
        mousePos = self.getUpdateReturnMousePos(pygame.mouse)
        print('mousePos : ', mousePos)

        # then, move the player to that spot
        self.movePlayer(mousePos)





                

        