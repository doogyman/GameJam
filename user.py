import pygame
from enitity import Entity
class User(Entity):
    def __init__(self, x, y, groups: pygame.sprite.Group):
        super.__init__(x, y, groups)
        self.pos = pygame.Vector2(x, y)
        self.basic = 'hello world'
        self.mousePositions = ()

    def printPosition(self):
        print(self.pos)

    def getInput():
        
        for event in pygame.event.get():
            print(event)

            if event == pygame.MOUSEBUTTONDOWN:
                print('Clicked')
                

            



raltao = User()

while True:
    # raltao.printy()
    raltao.getInput()