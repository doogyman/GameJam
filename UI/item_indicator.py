import pygame 
import math
from spritesheet import get_sprite
class ItemIndicator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_indicator = True
        self.is_visible = False
        
        self.sheet = pygame.image.load('assets/item_indicator-Sheet.png').convert_alpha()
        
        self.indicator = [get_sprite(self.sheet, i, 8, 8, 0, 0, 0, 1) for i in range(2)]

        self.sprites = self.indicator
        self.initial_indicator = None
        self.frame_index = 0
        self.animation_speed = 2
        
        self.image: pygame.Surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_frect(topleft=(0, 0))
        
    def indicator_type(self, ore_type):
        if ore_type == 'aluminium': #this check what kind of material it is 
            return ore_type
        elif ore_type == 'lithium':
            return ore_type
            
    def animate(self, target_rect, dt):
        if not self.sprites:
            return
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0
        self.image = self.sprites[int(self.frame_index)]
        self.rect = self.image.get_frect(center=target_rect.center)
    
    def show(self, groups):
        self.add(groups)
        self.is_visible = True
    
    def hide(self):
        super().kill()
        self.is_visible = False
    
        