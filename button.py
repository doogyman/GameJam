import pygame

pygame.font.init() # you have to call this at the start if you want to use this model

class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.width = 260
        self.height = 50
        self.fontSize = 30
        self.button = pygame.rect.Rect((self.position[0], self.position[1]), (self.width, self.height))
        self.font = pygame.font.SysFont('Comic Sans MS', self.fontSize)

    def draw(self, game_surface):
        btn = pygame.draw.rect(game_surface, 'light gray', self.button, 0, 5)
        pygame.draw.rect(game_surface, 'dark gray', self.button, 5, 5)
        text = self.font.render(self.text, True, 'black')
        # print('(self.position[0], + 15, self.position[1] + 7) : ', self.position[0], + 15, self.position[1] + 7))
        game_surface.blit(text, (self.position[0] + 90, self.position[1]))
    
    def isColliding(self):
        # print('self.button : ', self.button)
        # print('pygame.mouse.get_pos() : ', pygame.mouse.get_pos())
        # print('pygame.mouse.get_pressed() : ', pygame.mouse.get_pressed())
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]: # if the mouse button is on the button and the left mouse button is down (True) then
            # print("you've collided and the thingy's pressed")
            return True
        else:
            return False