import asyncio
import pygame
from sprites import *
from groups import AllSprites 
from user import User
# from mouse import Mouse
from pytmx import load_pygame
from globals import *


pygame.init()


class Game:
    def __init__(self):
        # setup
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Stone Village")
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
        self.game_surface = pygame.Surface((BASEWIDTH, BASEHEIGHT))
        self.scaled_surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        self.running = True
        
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.ore_sprites = pygame.sprite.Group()
        
        # debugging
        self.isDebugging = False
        
        
        self.setup()

    def setup(self):
        self.map = load_pygame("assets/untitled.tmx")

        # load the Tile layer 1 (tiles) 
        for x, y, image in self.map.get_layer_by_name("ground1").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'ground1'}, self.all_sprites)

        for x, y, image in self.map.get_layer_by_name("ground2").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'ground2'}, self.all_sprites)

        for x, y, image in self.map.get_layer_by_name("shadow").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'shadow'}, self.all_sprites)

        for x, y, image in self.map.get_layer_by_name("walls1").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'wall'}, self.all_sprites)

        for x, y, image in self.map.get_layer_by_name("walls1.5").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'wall'}, self.all_sprites)

        for x, y, image in self.map.get_layer_by_name("walls2").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'wall'}, self.all_sprites)

        # load the collision boxes 
        for obj in self.map.get_layer_by_name('collisionBoxes'):
            surf = obj.image
            x, y = int(obj.x), int(obj.y)
            w, h = obj.width, obj.height

            CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))

        # load the player starting point
        for obj in self.map.get_layer_by_name('player'):
            print(obj.name)
            print(obj.x, obj.y)
            if obj.name == "User":
                self.user = User(obj.x, obj.y, self.all_sprites, self.collision_sprites, self.ore_sprites)

            # pygame.Surface((obj.width, obj.height))

        # load the ores
        for obj in self.map.get_layer_by_name('ores'):
            print('obj : ', obj)
            x, y = int(obj.x), int(obj.y)
            w, h = int(obj.width), int(obj.height)
            ore_type = obj.name
            
            MaterialSprite((x, y), obj.image, (self.all_sprites, self.ore_sprites), ore_type)
    def draw(self):  
        self.game_surface.fill((153, 145, 126))
        self.all_sprites.draw(self.game_surface, self.user.rect.center)
        #self.user.draw(self.game_surface)
        # self.ground_sprites
        
        if self.isDebugging:
            self.debug()

        width, height = pygame.display.get_surface().get_size()
        print('w, h : ', width, height)

        self.scaled_surface = pygame.Surface((width, height))
        pygame.transform.scale(self.game_surface, (width, height), self.scaled_surface)
        self.screen.blit(self.scaled_surface, (0, 0))
        pygame.display.flip()
    
    def debug(self):
        # print('debugging')
        # DEBUG: Draw red outlines for collision sprites
        # for sprite in self.collision_sprites:
        #     self.all_sprites.drawHitbox(self.game_surface, self.user.rect.center)
        self.all_sprites.drawHitbox(self.game_surface, self.user.rect.center)
        
        # DEBUG: Draw green outline for the player
        offset = pygame.Vector2()
        offset.x = -(self.user.rect.center[0] - BASEWIDTH / 2)
        offset.y = -(self.user.rect.center[1] - BASEHEIGHT / 2)
        
        tempRect = pygame.Rect(self.user.hitbox_rect.x + offset.x, self.user.hitbox_rect.y + offset.y, self.user.hitbox_rect.width, self.user.hitbox_rect.height)
        pygame.draw.rect(self.game_surface, (0, 255, 0), tempRect, 1)


    async def run(self):
        while self.running:

            # keys = pygame.key.get_pressed()

            self.dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_F12:
                        print("running")
                        self.isDebugging = not self.isDebugging
            
            
            self.draw()

            self.user.update(self.dt)


            await asyncio.sleep(0)
async def main():
    game = Game()
    await game.run()

asyncio.run(main())

