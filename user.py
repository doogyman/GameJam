import pygame
from globals import *
from entity import Entity
from mouse import Mouse
from spritesheet import get_sprite
from UI.item_indicator import ItemIndicator
from UI.health_bar import *
from UI.effects.spotlight import SpotLight, Ambience
from UI.font import Font

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

        self.ore_indicator = ItemIndicator()
        self.font = Font('assets/font_sheet.png')
        self.sheet = pygame.image.load('assets/character-Sheet.png').convert_alpha()

        #battery
        self.battery_hp = 5 #secs
        self.health_bar = HealthBar(6, groups)
        self.battery_cells = []
        
        for i in range(6):
            self.cell = Cell(i, 6, groups)
            self.cell.set_pos(i)
            self.battery_cells.append(self.cell)
        self.battery_capacity = len(self.battery_cells)
        print("cells:", self.battery_cells)
        
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
        self.hitbox_rect = self.rect.inflate(-5, -20) # dest rect
        
        # movement
        self.is_moving = False
        self.direction = pygame.Vector2(0, 0)
        self.speed = 75
        self.diagonal_speed = math.sqrt(self.speed ** 2 / 2)
        self.collision_sprites = collision_sprites
        self.ore_sprites = ore_sprites
        
        self.radius = 25
    
       # self.ambience = Ambience(self.radius, self.groups()[0])
        
        #self.ambience.cut_hole(self.rect.center)
        
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
        prev_pos = self.pos.copy()
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        if self.direction.x != 0:
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox_rect.centerx = round(self.pos.x)
            self.collision('h')  # horizontal
        if self.direction.y != 0:
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox_rect.centery = round(self.pos.y)
            self.collision('v')  # vertical

        self.rect.center = self.hitbox_rect.center
        
        if (self.pos - prev_pos).length() / dt == 0:
            # print("actual speeed:", (self.pos - prev_pos).length() / dt )
            self.is_moving = False
        else:
            self.is_moving = True # this is to check whether the user is moving or not
            
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
                break
                #print(f"collision: {collision}")
        if collision:
            #print(f'Updating self.pos to: {self.rect.center}')
            self.pos = pygame.Vector2(self.hitbox_rect.center)

    def collide_with_ores(self):
        for sprite in self.ore_sprites:
            # print('1')
            if sprite.rect.colliderect(self.hitbox_rect):
                return sprite
        return None
    
    def update_indicator(self, dt):
        self.hovered_ore = self.collide_with_ores()
        if self.hovered_ore:
            # print(self.hovered_ore.ore_type)
            self.ore_indicator.indicator_type(self.hovered_ore.ore_type)
            self.font.render(self.hovered_ore.ore_type, (10, 10))
            self.ore_indicator.show(self.groups()[0])
            self.font.show(self.groups()[0])
            self.ore_indicator.animate(self.hovered_ore.rect, dt)
        else:
            self.ore_indicator.hide()
            
    def update_cells(self, dt):
        # print(f"capacity: {self.battery_capacity}")
        if self.is_moving and self.battery_hp > 0 and self.battery_capacity >= 0:
            self.battery_hp -= dt
            # print(f"battery_health: {self.battery_hp}")
        if self.battery_hp < 2 and self.battery_hp>0:
            # print("animation")
            self.cell.animate(dt)
        
        elif self.battery_capacity == 0:
            return None
                
        elif self.battery_hp <= 0 and self.battery_capacity >= 0:
            print("deleting")
            self.cell.hide()
            self.battery_cells.pop()
            self.battery_hp = 5
            index = len(self.battery_cells) - 1
            if index >= 0:
                self.cell = self.battery_cells[index]
                self.battery_capacity = len(self.battery_cells)
            else:
                return None
            index-=1
            
        
            
    def update(self, dt):
        self.input()
        self.move(dt)
        #self.ambience.update_cut_hole(self.rect, dt)
        self.animate(dt)
        self.update_cells(dt)
        self.update_indicator(dt)