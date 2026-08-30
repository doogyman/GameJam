import asyncio
import pygame
from sprites import *
from groups import AllSprites 
from user import User
from UI.effects.spotlight import Ambience
# from mouse import Mouse
from pytmx import load_pygame
from globals import *
from button import Button


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

        # for the main menu
        self.inMainMenu = True
        self.playButton = Button('play', (80, 80))
        
        
        
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
        
        for x, y, image in self.map.get_layer_by_name("doors").tiles():
            Sprite((x * TILESIZE, y * TILESIZE), image, {'groundType': 'door'}, self.all_sprites)

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
        for obj in self.map.get_layer_by_name('items'):
            print('obj : ', obj)
            x, y = int(obj.x), int(obj.y)
            w, h = int(obj.width), int(obj.height)
            item_type = obj.name
            
            MaterialSprite((x, y), obj.image, (self.all_sprites, self.ore_sprites), item_type)

    def draw(self, actualWidth, actualHeight):

        self.game_surface.fill((153, 145, 126))

        if not self.inMainMenu: # if drawing game
            self.all_sprites.draw(self.game_surface, self.user.rect.center)
        #self.user.draw(self.game_surface)
        # self.ground_sprites
        
        if self.isDebugging:
            self.debug()

        self.scaled_surface = pygame.Surface((actualWidth, actualHeight))
        pygame.transform.scale(self.game_surface, (actualWidth, actualHeight), self.scaled_surface)
        self.screen.blit(self.scaled_surface, (0, 0))

    def redoScreenSizings(self):
        # weird stuff to account for screen resizing and make it so that tile resolution stays the same
        actualWidth, actualHeight = pygame.display.get_surface().get_size()
        
        Globals.SCREENWIDTH = Globals.BASEWIDTH * Globals.SCALE #redo this cause SCALE could be changing if they've been scrolling in
        Globals.SCREENHEIGHT = Globals.BASEHEIGHT * Globals.SCALE #redo this cause SCALE could be changing if they've been scrolling in
        
        wMultiplier = actualWidth / Globals.SCREENWIDTH
        hMultiplier = actualHeight / Globals.SCREENHEIGHT
        width = BASEWIDTH * wMultiplier
        height = BASEHEIGHT * hMultiplier
        
        self.game_surface = pygame.Surface((width, height))

        return actualWidth, actualHeight

    def drawMainMenu(self, actualWidth, actualHeight):
        # print('drawMainMenu FUNC called')

        self.game_surface.fill((243, 243, 243))
        # button = pygame.rect.Rect((100, 100), (260, 40))
        # pygame.draw.rect(self.game_surface, 'dark gray', button, 5, 5)

        # print(self.playButton)

        self.playButton.draw(self.game_surface)


        # transfers stuff from game surface to screen surface to account for window resizing, then blits that onto the screen. crucial
        self.scaled_surface = pygame.Surface((actualWidth, actualHeight))
        pygame.transform.scale(self.game_surface, (actualWidth, actualHeight), self.scaled_surface)
        self.screen.blit(self.scaled_surface, (0, 0))

        
    def updateMainMenu(self):
        # print('updateMainMenu FUNC called')
        real_mouse_pos = pygame.mouse.get_pos()

        logic_mouse_pos = [None, None]
        logic_mouse_pos[0] = real_mouse_pos[0] / Globals.SCALE
        logic_mouse_pos[1] = real_mouse_pos[1] / Globals.SCALE

        
        # this is a function that updates the main menu
        if self.playButton.button.collidepoint((logic_mouse_pos[0], logic_mouse_pos[1])) and pygame.mouse.get_pressed()[0]: # if the mouse button is on the button and the left mouse button is down (True) then
            self.inMainMenu = False

    
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
                    elif event.key == pygame.K_o:
                        print('Globals.SCALE : ', Globals.SCALE)
                elif event.type == pygame.MOUSEWHEEL:
                    # print("event.x : ", event.x)
                    # print("event.y : ", event.y)
                    if not self.inMainMenu:
                        Globals.SCALE += (event.y * 0.05)
                        if Globals.SCALE <= 0: Globals.SCALE = 0.01


            actualWidth, actualHeight = self.redoScreenSizings()

            if not self.inMainMenu:
                self.user.update(self.dt)
                self.draw(actualWidth, actualHeight)
            elif self.inMainMenu:
                self.updateMainMenu()
                self.drawMainMenu(actualWidth, actualHeight)

            pygame.display.flip()


            await asyncio.sleep(0)
async def main():
    game = Game()
    await game.run()

asyncio.run(main())

