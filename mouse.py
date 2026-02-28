import pygame

class Mouse():

    def __init__(self, mouse):
        self.hello = 'world'
        self.pos = ()
        self.mouse = mouse

    def basic(self):
        print(self.hello)

    def getUpdateMousePos(self):
        newMousePos = self.mouse.get_pos()
        self.pos = newMousePos
        print('newMousePos : ', newMousePos)
        return newMousePos


