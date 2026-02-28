import pygame

class User:

    def __init__(self):
        self.basic = 'hello world'
        self.mousePositions = ()

    def printy(self):
        print(self.basic)

    def getInput():
        
        for event in pygame.event.get():
            print(event)

            if event == pygame.MOUSEBUTTONDOWN:
                print('Clicked')
                

            



raltao = User()

while True:
    # raltao.printy()
    raltao.getInput()