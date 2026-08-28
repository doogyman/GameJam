from globals import *

class SpotLight(pygame.sprite.Sprite):
    def __init__(self, target, radius, *groups):
        super().__init__(*groups)
        self.is_effect = True
        self.target_rect = target
        
        self.radius = radius
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.rect.center = self.target_rect.center
        
class Ambience(pygame.sprite.Sprite):
    def __init__(self, size, radius, *groups):
        super().__init__(*groups)
        self.r = radius
        self.is_ambience = True
        self.pos = pygame.Vector2(0, 0)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(topleft = self.pos)
        pygame.draw.rect(self.image, (38, 28, 38, 251), self.rect)
        self.reset()
        
    def reset(self):
        self.image.fill((38, 28, 38, 251))
    
    def cut_hole(self, target):
        self.target_surf = pygame.Surface(target)
        for r in range(self.r, 0, -1):
            alpha = int((1 - r/ self.r) * 251)
            pygame.draw.circle(self.image, (0, 0, 0, alpha), target, self.r)
            
        
    def update_cut_hole(self, target, dt=None):
        self.reset()
        self.cut_hole(target.center)
        
        