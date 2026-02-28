from globals import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # self.offset = pygame.Vector2(x, y)
    
    def draw(self, surface, target_pos):
        self.offset.x = -(target_pos[0] - BASEWIDTH / 2)
        self.offset.y = -(target_pos[1] - BASEHEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                surface.blit(sprite.image, sprite.rect.topleft + self.offset)