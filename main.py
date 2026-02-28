import asyncio
import pygame

from pytmx.util_pygame import load_pygame

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
        self.collision_sprites = pygame.sprite.Group()
        
        self.user = User(20, 20, self.all_sprites, self.collision_sprites)

        tmx_data = load_pygame('assets/firstMap.tmx')
        # print(dir(tmx_data))
        print(tmx_data)


 
    def draw(self):  
        self.game_surface.fill((50, 50, 50))
        scaled = pygame.transform.scale(self.game_surface, (SCREENWIDTH, SCREENHEIGHT))
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()


    async def run(self):
        # self.user.printPosition()
        while self.running:
            self.user.printPosition()

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


                self.user.checkInputs(event);
                

                
                    
            
            # self.user.update(keys)


                # self.user.update(self.dt)
            
            self.draw()

            await asyncio.sleep(0)








async def main():
    game = Game()
    await game.run()


    


asyncio.run(main())

