import pygame
from entity import Entity
from mouse import Mouse
from load_image import load_image
from spritesheet import get_sprite



class User(Entity):

    def __init__(self, x, y, groups: pygame.sprite.Group, collision_sprites: pygame.sprite.Group):
        
        super().__init__(x, y, groups)

        self.mouse = Mouse(pygame.mouse)
        self.pos = pygame.math.Vector2(x, y)
        self.pos = pygame.math.Vector2(x, y)
        # self.image
        self.basic = 'hello world'
        self.mousePositions = ()

        self.sheet = pygame.image.load('assets/pixilart-sprite.png').convert_alpha()

        self.idle_front = get_sprite(self.sheet, 1, 16, 32, 0, 0, 0, 1)
        self.idle_left = get_sprite(self.sheet, 5, 16, 32, 0, 0, 0, 1)
        self.idle_right = get_sprite(self.sheet, 9, 16, 32, 0, 0, 0, 1)
        self.idle_down = get_sprite(self.sheet, 13, 16, 32, 0, 0, 0, 1)

        self.walk_front = [get_sprite(self.sheet, i, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_left = [get_sprite(self.sheet, i + 4, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_right = [get_sprite(self.sheet, i + 8, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_back = [get_sprite(self.sheet, i + 12, 16, 32, 0, 0, 0, 1) for i in range(4)]

        self.currentXvelocity = 0
        self.currentYvelocity = 0

        self.velocityRate = 5




    def checkInputs(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = self.getUpdateReturnMousePos()
            self.movePlayer(pos)
            print(self.pos[0], self.pos[1])
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print('w pressed')
                self.currentYvelocity = self.velocityRate
            elif event.key == pygame.K_s:
                print('s pressed')                
                self.currentYvelocity = -self.velocityRate
            elif event.key == pygame.K_a:
                print('a pressed')                
                self.currentXvelocity = -self.velocityRate
            elif event.key == pygame.K_d:
                print('d pressed')                
                self.currentXvelocity = self.velocityRate
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                print('w released')
                self.yVelocity = 0
            elif event.key == pygame.K_s:
                print('s released')
                self.yVelocity = 0
            elif event.key == pygame.K_a:
                print('a released')
                self.currentXvelocity = 0
            elif event.key == pygame.K_d:
                print('d released')
                self.currentXvelocity = 0

    def movePlayer(self, mousePos):
        self.pos = pygame.math.Vector2(mousePos[0], mousePos[1])
        print('self.pos : ', self.pos)

    def getUpdateReturnMousePos(self):
        mousePos = self.mouse.getUpdateMousePos()
        return mousePos

    def update(self):
        self.pos[0] += self.currentXvelocity
        self.pos[1] += self.currentYvelocity

    def printPosition(self):
        print(self.pos)
    
    
    
    






