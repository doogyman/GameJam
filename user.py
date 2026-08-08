import pygame
from globals import *
from entity import Entity
from mouse import Mouse
from spritesheet import get_sprite

from UI.ore_indicator import OreIndicator


class User(Entity):

    def __init__(self, x, y, groups: pygame.sprite.Group, collision_sprites: pygame.sprite.Group, ore_sprites: pygame.sprite.Group):
        super().__init__(x, y, groups)

        print('User constructor')
        print('x : ', x)
        print('y : ', y)
        self.mouse = Mouse(pygame.mouse)
        self.pos = pygame.math.Vector2(x, y)
        self.basic = 'hello world'
        self.mousePositions = ()
    
        # for picking up things
        self.items = {
            'aluminium' : 0,
            'lithium' : 0
        }
        self.hovered_ore = None

        self.ore_indicator = OreIndicator()

        self.sheet = pygame.image.load('assets/character-Sheet.png').convert_alpha()
        

        """self.aluminiumMessageBoxesSheet = pygame.image.load('assets/titanium-Sheet.png').convert_alpha()
        self.aluminiumMessageBoxList = [get_sprite(self.aluminiumMessageBoxesSheet, i, 40, 16, 0, 0, 0, 2) for i in range(10)]
        self.oreCounter = 0
        self.messageIndex = 0 # for controlling which frame of the animation is currently playing

        self.lithiumMessageBoxesSheet = pygame.image.load('assets/titanium-Sheet.png').convert_alpha()
        self.lithiumMessageBox = [get_sprite(self.lithiumMessageBoxesSheet, i, 40, 16, 0, 0, 0, 2) for i in range(10)]"""

        # health/battery bar
        
        self.battery = float(1) # float from 0-1
        


        self.idle_front = [get_sprite(self.sheet, 1, 16, 32, 0, 0, 0, 1)]
        self.idle_right = [get_sprite(self.sheet, 5, 16, 32, 0, 0, 0, 1)]
        self.idle_left = [get_sprite(self.sheet, 9, 16, 32, 0, 0, 0, 1)]
        self.idle_back = [get_sprite(self.sheet, 13, 16, 32, 0, 0, 0, 1)]

        self.walk_front = [get_sprite(self.sheet, i, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_right = [get_sprite(self.sheet, i + 4, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_left = [get_sprite(self.sheet, i + 8, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_back = [get_sprite(self.sheet, i + 12, 16, 32, 0, 0, 0, 1) for i in range(4)]

        # print('self.walk_front : ', self.walk_front[0])

        self.status = 'front'
        self.frame_index = 0
        self.animation_speed = [float(3), float(7.5)]  # [idle, walk]
        # set the initial image and rect
        self.image: pygame.Surface = self.idle_front[0]
        self.rect = self.image.get_rect(center=self.pos) # source rect
        self.hitbox_rect = self.rect.inflate(-5, -15) # dest rect
        # movement
        self.direction = pygame.Vector2(0, 0)
        self.speed = 100
        self.diagonal_speed = math.sqrt(self.speed ** 2 / 2)
        self.collision_sprites = collision_sprites
        self.ore_sprites = ore_sprites

    def input(self):
            keys = pygame.key.get_pressed()
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

            if keys[pygame.K_o] and self.hovered_ore:
                print('o is pressed!')
                print('self.hovered_ore : ', self.hovered_ore)
                if (self.hovered_ore.ore_type == 'aluminium'):
                    print('picked up aluminium')
                    self.items['aluminium'] += 1
                elif (self.hovered_ore.ore_type == 'lithium'):
                    print('picked up lithium')
                    self.items['lithium'] += 1
                
                else:
                    print('something went kinda wrong')
                

                self.hovered_ore.kill()


            #print(f"Direction: {self.direction}")
            
    def move(self, dt):
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        if self.direction.x != 0:

            print("speed", self.speed)
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox_rect.centerx = int(self.pos.x)
            self.collision('h')  # horizontal

        if self.direction.y != 0:
        
            print("speed", self.speed)
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox_rect.centery = int(self.pos.y)
            self.collision('v')  # vertical
        self.rect.center = self.hitbox_rect.center
    

    def animate(self, dt):
        if self.direction.x > 0:
            self.status = "right"; sprites = self.walk_right
        elif self.direction.x < 0:
            self.status = "left"; sprites = self.walk_left
        elif self.direction.y > 0:
            self.status = "front"; sprites = self.walk_front 
        elif self.direction.y < 0:
            self.status = "back"; sprites = self.walk_back
        elif self.direction.x == 0 and self.direction.y == 0:
            sprites = getattr(self, f"idle_{self.status}")
        
        speed = self.animation_speed[0] if self.direction.x == 0 and self.direction.y == 0 else self.animation_speed[1]
        self.frame_index += speed * dt
        if self.frame_index >= len(sprites):
            self.frame_index = 0
        
        self.image = sprites[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def collision(self, direction):
        collision = False
        # print('self.hitbox_rect : ', self.hitbox_rect)
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                # print('sprite.rect : ', sprite.rect)

                collision = True
                #print(f'COLLISION in {direction} with: {sprite}, rect: {sprite.rect}, player: {self.rect}')
                if direction == 'h':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'v':
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                #print(f"collision: {collision}")
        if collision:
            #print(f'Updating self.pos to: {self.rect.center}')
            self.pos = pygame.Vector2(self.hitbox_rect.center)

    def collide_with_ores(self):
        for sprite in self.ore_sprites:
            # print('1')
            if sprite.rect.colliderect(self.hitbox_rect):
                return sprite
        # self.hovered_ore = None
        return None

    """def draw(self, surface):
        print('USER DRAW method special overwritten version of class method')

        for sprite in self.ore_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                
                # self.oreCounter += 1

                # if self.oreCounter >= 2: # arbitrary value deciding how often message box animation changes
                #     self.oreCounter = 0
                #     self.messageIndex += 1

                #     if self.messageIndex >= 10:
                #         self.messageIndex = 0

                print("collided with ore")

                sprite.collidedWithPlayer(surface, self.aluminiumMessageBoxList, self.rect)
            """
    
    def update_indicator(self, dt):
        self.hovered_ore = self.collide_with_ores()
        if self.hovered_ore:
            print(self.hovered_ore.ore_type)
            self.ore_indicator.indicator_type(self.hovered_ore.ore_type)
            self.ore_indicator.animate(self.hovered_ore.rect, dt)
            self.ore_indicator.show(self.groups()[0])
        else:
            self.ore_indicator.hide()
        
                
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.update_indicator(dt)


    def printPosition(self):
        print(self.pos)

    def getUpdateReturnMousePos(self):
        mousePos = self.mouse.getUpdateMousePos()
        return mousePos
    
    def movePlayer(self, mousePos):
        self.pos = pygame.math.Vector2(mousePos[0], mousePos[1])
        print('self.pos : ', self.pos)


    def moveToMouse(self):
        #first step is to get the mouse coords
        mousePos = self.getUpdateReturnMousePos(pygame.mouse)
        print('mousePos : ', mousePos)

        # then, move the player to that spot
        self.movePlayer(mousePos)





                

        