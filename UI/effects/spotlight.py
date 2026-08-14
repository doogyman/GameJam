from globals import *

class SpotLight(pygame.sprite.Sprite):
    def __init__(self, target_x, target_y, radius, *groups):
        super().__init__(*groups)
        self.is_effect = True
        self.x = target_x
        self.y = target_y
        self.pos = pygame.Vector2(self.x, self.y)
        
        self.radius = radius
        
        w = h = self.radius * 2
        
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        
        self.rect = self.image.get_frect(center=self.pos)
        pygame.draw.circle(self.image, (255, 255, 255, 0), (self.radius, self.radius), self.radius)
            
        
    
class Ambience(pygame.sprite.Sprite):
    def __init__(self, w, h, *groups):
            super().__init__(groups)
            self.is_ambience = True
            self.w = w
            self.h = h
            self.pos = pygame.Vector2(0, 0)
            self.image = pygame.Surface((Globals.SCREENWIDTH, Globals.SCREENHEIGHT), pygame.SRCALPHA)
            self.rect = self.image.get_frect(topleft = self.pos)
            pygame.draw.rect(self.image, (38, 28, 38, 240), self.rect)
            