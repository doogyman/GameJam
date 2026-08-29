from globals import *
from spritesheet import clip
class Font:
    def __init__(self, sheet, *groups):
        super().__init__(groups)
        self.charater_order = list('abcdefghijklmopqrstuwvxyz') + list('0123456789')
        self.spacing = 1
        self.font_sheet = pygame.image.load(sheet).convert_alpha()
        current_character_width = 0
        self.characters = {}
        counter = 0
        for x_coord in range(self.font_sheet.get_width()):
            color = self.font_sheet.get_at(x_coord, 0)
            if color[0] == 105:
                char_img = clip(self.font_sheet, x_coord - current_character_width, 0, current_character_width, self.font_sheet.get_height())
                self.characters[self.charater_order[counter]] = char_img.copy()
                counter += 1
                current_character_width = 0
            else:
                current_character_width += 1
    
    def draw(self, surf, text, loc):
        pass