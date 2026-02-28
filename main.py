import asyncio
import pygame

from groups import AllSprites 
from user import User
from mouse import Mouse
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
        
        self.user = User(20, 20, self.all_sprites)

 
    def draw(self):  
        self.game_surface.fill((50, 50, 50))
        scaled = pygame.transform.scale(self.game_surface, (SCREENWIDTH, SCREENHEIGHT))
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()


    async def run(self):
        while self.running:

            self.dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                # if event.type == 

                if event.type == pygame.KEYDOWN:
                    pass

                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_F12:
                        print("running")
                        self.debug_mode = not self.debug_mode
            
            self.draw()

            await asyncio.sleep(0)


mouse = Mouse(pygame.mouse)
# raltao = User()





async def main():
    game = Game()
    await game.run()



asyncio.run(main())

