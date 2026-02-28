import pygame
from entity import Entity
from mouse import Mouse



class User(Entity):

    def __init__(self, x, y, groups: pygame.sprite.Group):
        super().__init__(x, y, groups)

        self.mouse = Mouse(pygame.mouse)
        self.pos = (x, y)
        self.image
        self.basic = 'hello world'
        self.mousePositions = ()

    def printPosition(self):
        print(self.pos)

    def getUpdateReturnMousePos(self, mouse):
        mousePos = self.mouse.getUpdateMousePos()
        return mousePos
    
    def movePlayer(self, mousePos):
        self.pos = mousePos


    def moveToMouse(self):
        #first step is to get the mouse coords
        mousePos = self.getUpdateReturnMousePos(pygame.mouse)
        print('mousePos : ', mousePos)

        # then, move the player to that spot
        self.movePlayer(mousePos)





                

        