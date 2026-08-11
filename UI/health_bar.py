from globals import BASEHEIGHT as BASEHEIGHT, BASEWIDTH as BASEWIDTH, FPS as FPS, Globals as Globals, Path as Path, SCALE as SCALE, SCREENHEIGHT as SCREENHEIGHT, SCREENWIDTH as SCREENWIDTH, TILESIZE as TILESIZE, math as math, pygame as pygame
from spritesheet import get_sprite
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, capacity: int, *groups):
        super().__init__(groups)
        self.x = 5
        self.y = 5
        self.pos = pygame.math.Vector2(self.x, self.y)
        
        self.capacity = capacity
        self.is_health_bar = True
        self.is_visible = False
        
        self.image = pygame.image.load("assets/health_bar.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        
class Cell(HealthBar):
    def __init__(self, id, capacity, *groups):
        HealthBar.__init__(self, capacity, groups)
        
        self.id = id
        
        self.offset_x = 3
        self.offset_y = 6
        
        self.x = self.x + self.offset_x
        self.y = self.y + self.offset_y
        
        self.pos = pygame.Vector2(self.x, self.y)
        
        self.sheet = pygame.image.load("assets/cell-sheet.png")
        self.cell_flash = [get_sprite(self.sheet, i, 6, 4, 0, 0, 0, 1) for i in range(2)]
        self.cell_normal = get_sprite(self.sheet, 0, 6, 4, 0, 0, 0, 1)
        
        self.image = self.cell_normal
        self.rect = self.image.get_rect(topleft=self.pos)
        
        self.status = 'healthy'
        
        self.frame_index = 0
        self.animation_speed = 2
        
    def set_pos(self, index, increment=6):
        offset = index * increment
        self.pos.x += offset
        
        self.rect.topleft = self.pos
        print(self.rect.topleft)
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.cell_flash):
            self.frame_index = 0
            
        self.image = self.cell_flash[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)
    #TODO do animation when the time is 80% complete
    def hide(self):
        super().kill()
        self.is_visible = False