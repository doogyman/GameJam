from globals import *
from spritesheet import clip
class Font(pygame.sprite.Sprite):
    def __init__(self, sheet):
        self.is_text = True
        self.is_visible = False
        self.charater_order = list('abcdefghijklmnopqrstuwvxyz') + list('0123456789')
        self.spacing = 1
        self.font_sheet = pygame.image.load(sheet).convert_alpha()
        current_character_width = 0
        self.characters = {}
        counter = 0
        # This basically add all the characters in a dictionary of surfaces, as one surface is assigned to a character.
        for x_coord in range(self.font_sheet.get_width()):
            color = self.font_sheet.get_at((x_coord, 0))
            if color[0] == 105:
                char_image = clip(self.font_sheet, x_coord - current_character_width, 0, current_character_width, self.font_sheet.get_height())
                self.characters[self.charater_order[counter]] = char_image.copy()
                counter += 1
                current_character_width = 0
            else:
                current_character_width += 1
                
    
    def render(self,  text, loc):
        w = 0
        for ch in text:
            width_of_character = self.characters[ch].get_width()
            w = w + width_of_character + self.spacing
        h = self.font_sheet.get_height()
        
        character_surf = pygame.Surface((w, h))
        
        x_offset = 0
        for ch in text:
            char_img = self.characters[ch]
            character_surf.blit(char_img, (loc[0] + x_offset, loc[1]))
            x_offset += char_img.get_width() + self.spacing
        
        return character_surf
    
    def show(self, groups):
            self.add(groups)
            self.is_visible = True
        
    def hide(self):
            super().kill()
            self.is_visible = False