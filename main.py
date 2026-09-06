import asyncio
import pygame
from sprites import *
from groups import AllSprites 
from user import User
from UI.effects.spotlight import Ambience
# from mouse import Mouse
from pytmx import load_pygame
from globals import *
from buttons import *
from UI.font import Font

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
        self.playButton = Picture_Button('assets/play.png', (150, 50), 4) # arbritrary starting numbers because gets updated every frame of the main menu anyways

        self.allLevelsButton = Picture_Button('assets/all_levels.png', (150, 100), 4) # arbritrary starting numbers because gets updated every frame of the main menu anyways


        # for the pause menu
        self.isPaused = False # if in the main menu, ignore the value of this anyway
        self.pauseButton = Picture_Button('assets/pause.png', (SCREENWIDTH - 10, SCREENHEIGHT - 10), (1/4))

        self.fontSize = 30
        self.font = pygame.font.SysFont('Comic Sans MS', self.fontSize)
    
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
        for obj in self.map.get_layer_by_name('items'):
            print('obj : ', obj)
            x, y = int(obj.x), int(obj.y)
            w, h = int(obj.width), int(obj.height)
            item_type = obj.name
            
            MaterialSprite((x, y), obj.image, (self.all_sprites, self.ore_sprites), item_type)

    def update(self, dt):
        # print('update FUNC called')
        self.user.update(dt)

        real_mouse_pos = pygame.mouse.get_pos()


        # print('self.pauseButton.button : ', self.pauseButton.button)
        # print('real_mouse_pos : ', real_mouse_pos)
        if self.pauseButton.button.collidepoint(real_mouse_pos) and pygame.mouse.get_pressed()[0]:
            # print('trying to pause the game')
            self.isPaused = True


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

        # update the position of incase of screen resizing and draw the pause button
        newPauseButtonPos = pygame.display.get_surface().get_size()
        # print('newPauseButtonPos : ', newPauseButtonPos)
        # print(int(newPauseButtonPos[0] - 10), int(newPauseButtonPos[1] - 10))
        # self.pauseButton.button[0] = (int(newPauseButtonPos[0] - 10), int(newPauseButtonPos[1] - 10))
        # print(self.pauseButton.button)
        # print(self.pauseButton.button.x)

        self.pauseButton.button.x = (newPauseButtonPos[0] - 10 - 50) # 50 being the assumed width of the button at (1/4) its original size
        self.pauseButton.button.y = 10
        self.pauseButton.draw(self.scaled_surface)

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
        # transfers stuff from game surface to screen surface to account for window resizing, then blits that onto the screen. crucial
        self.scaled_surface = pygame.Surface((actualWidth, actualHeight))
        pygame.transform.scale(self.game_surface, (actualWidth, actualHeight), self.scaled_surface)

        self.playButton.draw(self.scaled_surface)
        self.allLevelsButton.draw(self.scaled_surface)

        self.screen.blit(self.scaled_surface, (0, 0))

        
    def updateMainMenu(self):

        # define the current screen height and width because they are used to reposition both the update button and all levels button and also it's better to have one copy of the window sizes incase the window gets resized in the middle of this func
        currentScreenHeight = pygame.display.get_surface().get_height()
        currentScreenWidth = pygame.display.get_surface().get_width()

        # update play button
        playButtonWidth = self.playButton.image.get_width()
        playButtonHeight = self.playButton.image.get_height()

        self.playButton.button.x = ( currentScreenWidth -  playButtonWidth) / 2
        self.playButton.button.y = ( currentScreenHeight -  playButtonHeight) * (3 / 10)

        # update all levels button
        allLevelsButtonWidth = self.allLevelsButton.image.get_width()
        allLevelsHeight = self.allLevelsButton.image.get_height()
    
        self.allLevelsButton.button.x = ( currentScreenWidth -  allLevelsButtonWidth) / 2
        self.allLevelsButton.button.y = ( currentScreenHeight -  allLevelsHeight) * (6 / 10)




        real_mouse_pos = pygame.mouse.get_pos()
        # checks if the play button has been clicked
        if self.playButton.button.collidepoint(real_mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.inMainMenu = False

    def drawPauseMenu(self, actualWidth, actualHeight):
        # print('drawPauseMenu FUNC called')
        color = (179, 179, 179)

        width = (4/5) * actualWidth
        height = (4/5) * actualHeight
        x = (actualWidth - width) / 2
        y = (actualHeight - height) / 2

        rect = pygame.rect.Rect(x, y, width, height)

        unpauseButton = Text_Button('Unpause', ((x + (width / 2) - 90), (y + height - 50))) # 50 being some arbritary amount of pixels to lift it off the very bottom of the pause box by

        self.scaled_surface = pygame.Surface((actualWidth, actualHeight))
        pygame.transform.scale(self.game_surface, (actualWidth, actualHeight), self.scaled_surface)

        # (load and )blit things here because its not part of the game is on a layer on top
        text = self.font.render('Game Paused', True, (255, 255, 255))

        pygame.draw.rect(self.scaled_surface, color, rect)
        self.scaled_surface.blit(text, ((x + (width / 2) - 90), (y + 10)) ) # 45 being estimated half of width of text 'Game Paused'
        unpauseButton.draw(self.scaled_surface)


        self.screen.blit(self.scaled_surface, (0, 0))

        return unpauseButton

    def updatePauseMenu(self, unpauseButton):
        # print('updatePauseMenu FUNC called')

        # print('updateMainMenu FUNC called')
        real_mouse_pos = pygame.mouse.get_pos()
        
        
        
        # this is a function that updates the main menu
        if unpauseButton.button.collidepoint(real_mouse_pos) and pygame.mouse.get_pressed()[0]: # if the mouse button is on the button and the left mouse button is down (True) then
            self.isPaused = False
    
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

            if  self.inMainMenu:
                self.updateMainMenu()
                self.drawMainMenu(actualWidth, actualHeight)
            elif not self.inMainMenu:
                if not self.isPaused:
                    self.update(self.dt)
                    self.draw(actualWidth, actualHeight)
                elif self.isPaused:
                    self.draw(actualWidth, actualHeight)
                    unpauseButton = self.drawPauseMenu(actualWidth, actualHeight)
                    self.updatePauseMenu(unpauseButton)


            pygame.display.flip()


            await asyncio.sleep(0)
async def main():
    game = Game()
    await game.run()

asyncio.run(main())

