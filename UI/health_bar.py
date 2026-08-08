from globals import *

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(groups)
        self.x = 5
        self.y = 5
        self.is_health_bar = True
        self.pos = pygame.math.Vector2(self.x, self.y)
        
        self.image = pygame.image.load("assets/health_bar.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        
        