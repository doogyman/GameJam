from globals import *
from spritesheet import get_sprite
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, id, *groups):
        super().__init__(groups)
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
        HealthBar.__init__(self, id, groups)
        self.cells = []
        
        self.offset_x = 3
        self.offset_y = 6
        
        self.cell_x = self.x + self.offset_x
        self.cell_y = self.y + self.offset_y
        
        self.cell_pos = pygame.Vector2(self.cell_x, self.cell_y)
        
        self.sheet = pygame.image.load("assets/cell-sheet.png")
        self.cell_flash = [get_sprite(self.sheet, i, 6, 4, 0, 0, 0, 1) for i in range(2)]
        self.cell_normal = get_sprite(self.sheet, 0, 6, 4, 0, 0, 0, 1)
        
        self.image = self.cell_normal
        self.rect = self.image.get_rect(topleft=self.pos)
        
        self.status = 'healthy'
        
    def set_pos(self, index, increment=6):
        self.pos.x += increment * index
        self.pos.y = self.cell_y
        
        self.rect.topleft  = self.pos
        
    #TODO do animation when the time is 80% complete
        
        