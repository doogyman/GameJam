from globals import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.Vector2()
        
        self.ground_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()
        self.indicator_sprites = pygame.sprite.Group()
        self.battery = pygame.sprite.Group()
        self.ambience = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        
    def catagorise(self):
        # print('beginning of categorise, len(self.indicator_sprites) : ', len(self.indicator_sprites))
        # pygame sprite groups only hold unique sprites; adding a sprite to a group more than once won't make it appear twice in the list. Code below works

        for sprite in self:
            if hasattr(sprite, 'ground'):
                self.ground_sprites.add(sprite)
            elif hasattr(sprite, 'is_indicator'):
                self.indicator_sprites.add(sprite)
            elif hasattr(sprite, 'is_health_bar'):
                self.battery.add(sprite)
            elif hasattr(sprite, 'is_ambience'):
                self.ambience.add(sprite)
            elif hasattr(sprite, 'is_effect'):
                self.effects.add(sprite)
            else:
                self.object_sprites.add(sprite)

        # print('end of categorise, len(self.indicator_sprites) : ', len(self.indicator_sprites))

        
    def draw(self, surface, target_pos):
        width = surface.width
        height = surface.height

        self.offset.x = -(target_pos[0] - width / 2)
        self.offset.y = -(target_pos[1] - height / 2)
        
        self.catagorise()

        # blit ground sprites which aren't walls
        for sprite in self.ground_sprites:
            if sprite.groundType != 'wall' and not hasattr(sprite, 'is_effect'):
                surface.blit(sprite.image, sprite.rect.topleft + self.offset)
            # print('sprite.groundType !! : ', sprite.groundType)

        # check if sprite is not a ground sprite because we've already blitted those and not a indicator sprite because we're about to blit those (and ore splits aren't blit in this part of the game btw)
        counter = 0
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            if hasattr(sprite, 'ground') and sprite.groundType != 'wall':
                continue
            elif hasattr(sprite, 'is_indicator'):
                continue
            elif hasattr(sprite, 'is_ambience'):
                continue
            elif hasattr(sprite, 'is_effect'):
                continue
            else:
                # print(counter, ' ', sprite.rect.centery)
                surface.blit(sprite.image, sprite.rect.topleft + self.offset)
                counter += 1
        
        #blitting indicator sprites
        otherOffset = pygame.Vector2()
        otherOffset.x = 0
        otherOffset.y = -3
        for sprite in self.indicator_sprites:
            coords = (sprite.rect.x + self.offset.x + otherOffset.x, sprite.rect.y + self.offset.y + otherOffset.y)
            # print("loading")
            surface.blit(sprite.image, coords)

        for sprite in self.ambience:
            surface.blit(sprite.image, sprite.rect.topleft + self.offset)
            
        for sprite in self.battery:
            surface.blit(sprite.image, sprite.rect.topleft)
            
    def drawHitbox(self, surface, target_pos):
        self.offset.x = -(target_pos[0] - BASEWIDTH / 2)
        self.offset.y = -(target_pos[1] - BASEHEIGHT / 2)

        # ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        player_sprite = [sprite for sprite in self if hasattr(sprite, 'Player')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground') and not hasattr(sprite, 'is_visible')]
        indicator_sprites = [sprite for sprite in self if hasattr(sprite, 'is_visible')]

        # print('object_sprites : ', object_sprites)

        # for sprite in ground_sprites:
        #     # print('spritey : ', sprite.rect)

        #     rect = pygame.Rect(sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height)

        #     pygame.draw.rect(surface, (0, 0, 0), rect, width=1)
        otherOffset = pygame.Vector2()
        otherOffset.x = 0
        otherOffset.y = -3
        for sprite in indicator_sprites:
            rect = pygame.Rect(sprite.rect.x + self.offset.x + otherOffset.x, sprite.rect.y + self.offset.y + otherOffset.y, sprite.rect.width, sprite.rect.height)
        
            pygame.draw.rect(surface, (0, 0, 0), rect, width=1)

        for sprite in sorted(object_sprites, key=lambda sprite: sprite.rect.centery):
            # print('spritey : ', sprite.rect)

            rect = pygame.Rect(sprite.rect.x + self.offset.x, sprite.rect.y + self.offset.y, sprite.rect.width, sprite.rect.height)

            pygame.draw.rect(surface, (0, 0, 0), rect, width=1)