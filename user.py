import pygame
from entity import Entity
from mouse import Mouse
from load_image import load_image
from spritesheet import get_sprite



class User(Entity):

    def __init__(self, x, y, groups: pygame.sprite.Group, collision_sprites: pygame.sprite.Group):
        super().__init__(x, y, groups)

        self.mouse = Mouse(pygame.mouse)
        self.pos = pygame.math.Vector2(x, y)
        self.image
        self.basic = 'hello world'
        self.mousePositions = ()

        self.sheet = pygame.image.load('assets/pixilart-sprite.png').convert_alpha()

        self.idle_front = get_sprite(self.sheet, 1, 16, 32, 0, 0, 0, 1)
        self.idle_left = get_sprite(self.sheet, 5, 16, 32, 0, 0, 0, 1)
        self.idle_right = get_sprite(self.sheet, 9, 16, 32, 0, 0, 0, 1)
        self.idle_back = get_sprite(self.sheet, 13, 16, 32, 0, 0, 0, 1)

        self.walk_front = [get_sprite(self.sheet, i, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_left = [get_sprite(self.sheet, i + 4, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_right = [get_sprite(self.sheet, i + 8, 16, 32, 0, 0, 0, 1) for i in range(4)]
        self.walk_back = [get_sprite(self.sheet, i + 12, 16, 32, 0, 0, 0, 1) for i in range(4)]

        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = [float(3), float(7.5)]  # [idle, walk]
        # set the initial image and rect
        self.image: pygame.Surface = self.idle_front
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox_rect = self.rect.inflate(-10, -30)
        # movement
        self.direction = pygame.Vector2(0, 0)
        self.speed = 100
        self.collision_sprites = collision_sprites


        

    def input(self):
            keys = pygame.key.get_pressed()
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

            #print(f"Direction: {self.direction}")
            
    def move(self, dt):

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox_rect.centerx = int(self.pos.x)
        self.collision('h') # horizontal
        self.pos.y += self.direction.y * self.speed * dt
        
        self.hitbox_rect.centery = int(self.pos.y)
        self.collision('v') # vertical
        self.rect.center = self.hitbox_rect.center


    def animate(self, dt):
        if self.direction.x > 0:
            self.status = "right"; sprites = self.walk_right
        elif self.direction.x < 0:
            self.status = "left"; sprites = self.walk_left
        elif self.direction.y > 0:
            self.status = "down"; sprites = self.walk_front 
        elif self.direction.y < 0:
            self.status = "up"; sprites = self.walk_back
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
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
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

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)




    def printPosition(self):
        print(self.pos)

    def getUpdateReturnMousePos(self, mouse):
        mousePos = self.mouse.getUpdateMousePos()
        return mousePos
    
    def movePlayer(self, mousePos):
        self.pos = mousePos


    def moveToMouse(self):
        #first step is to get the mouse coords
        mousePos = self.getUpdateReturnMousePos(pygame.mouse)
        print('mousePos : ', mousePos)

        # then, move the player to that spot
        self.movePlayer(mousePos)





                

        