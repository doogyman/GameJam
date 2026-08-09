from globals import *

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, id, *groups):
        super().__init__(id, groups)
        self.x = 5
        self.y = 5
        self.id = id
        
        self.is_health_bar = True
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.cells = []
        
        self.image = pygame.image.load("assets/health_bar.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        
class Cells(HealthBar):
    def __init__(self, id, *groups):
        HealthBar.__init__(id, groups)
        self.cells = []
        #TODO pirn each of the follwing cells based on the id of the battery capcaity
