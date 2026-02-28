import asyncio
import pygame
from sprites import *
from groups import AllSprites 
from user import User
from mouse import Mouse
from pytmx import load_pygame
from globals import *
pygame.init()





class Game:
    def __init__(self):
        # setup
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Stone Village")
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.game_surface = pygame.Surface((BASEWIDTH, BASEHEIGHT))
        self.running = True

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup()

    def setup(self):
        self.map = load_pygame("assets/firstMap.tmx")

        for x, y, image in self.map.get_layer_by_name("Tile Layer 1").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, self.all_sprites)

        for obj in self.map.get_layer_by_name('Object Layer 1'):
            surf = obj.image
            x, y = int(obj.x), int(obj.y)
            w, h = obj.width, obj.height

            CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))

            if obj.name == 'Player':
                print('yes obj.name == player')
                self.user = User((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.all_sprites, self.collision_sprites)

    def draw(self):  
        self.game_surface.fill((0, 0, 0))
        self.all_sprites.draw(self.game_surface, self.user.rect.center)
        scaled = pygame.transform.scale(self.game_surface, (SCREENWIDTH, SCREENHEIGHT))
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()


    async def run(self):
        self.dt = self.clock.tick(FPS) / 1000
        # self.user.printPosition()
        while self.running:

            # keys = pygame.get.key.get_pressed()

            # self.dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_F12:
                        print("running")
                        self.debug_mode = not self.debug_mode
            self.user.update(self.dt)
            
            self.draw()

            await asyncio.sleep(0)








async def main():
    game = Game()
    await game.run()


    


asyncio.run(main())

