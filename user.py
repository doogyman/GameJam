import pygame
from entity import Entity
class User(Entity):

    def __init__(self, x, y, groups: pygame.sprite.Group):
        super().__init__(x, y, groups)
        self.startingPos = pygame.Vector2(x, y)
        self.pos = ()
        self.basic = 'hello world'
        self.mousePositions = ()

    def printPosition(self):
        print(self.pos)

    def getUpdateReturnMousePos(self, mouse):
        mousePos = mouse.get_pos()
        return mousePos
    
    def movePlayer(self, mousePos):
        self.pos = mousePos


    def moveToMouse(self):
        #first step is to get the mouse coords
        mousePos = self.getUpdateReturnMousePos(pygame.mouse)
        print('mousePos : ', mousePos)

        # then, move the player to that spot
        self.movePlayer(mousePos)





                

        