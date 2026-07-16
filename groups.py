from globals import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.Vector2()
    
    def draw(self, surface, target_pos):
        self.offset.x = -(target_pos[0] - BASEWIDTH / 2)
        self.offset.y = -(target_pos[1] - BASEHEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for sprite in ground_sprites:
            surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        for sprite in sorted(object_sprites, key=lambda sprite: sprite.rect.centery):
            surface.blit(sprite.image, sprite.rect.topleft + self.offset)
    
    def drawHitbox(self, surface, target_pos):
        self.offset.x = -(target_pos[0] - BASEWIDTH / 2)
        self.offset.y = -(target_pos[1] - BASEHEIGHT / 2)

        # ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]
        player_sprite = [sprite for sprite in self if hasattr(sprite, 'Player')]

        print('object_sprites : ', object_sprites)

        # for sprite in ground_sprites:
        #     # print('spritey : ', sprite.rect)

        #     rect = pygame.Rect(sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)

        #     pygame.draw.rect(surface, (0, 0, 0), rect, width=1)

        for sprite in sorted(object_sprites, key=lambda sprite: sprite.rect.centery):
            # print('spritey : ', sprite.rect)

            rect = pygame.Rect(sprite.rect.x + self.offset.x, sprite.rect.y + self.offset.y, sprite.rect.width, sprite.rect.height)

            pygame.draw.rect(surface, (0, 0, 0), rect, width=1)