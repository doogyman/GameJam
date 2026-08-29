from globals import *
from spritesheet import clip
class Font:
    def __init__(self, sheet, *groups):
        super().__init__(groups)
        self.charater_order = list('abcdefghijklmopqrstuwvxyz') + list('0123456789')
        self.spacing = 1
        self.font_sheet = pygame.image.load(sheet).convert_alpha()
        self.font_info = pygame.surfarray.array2d(self.font_sheet)
        self.charaters = {}
        for x_coord in range(self.font_sheet.get_width()):
            color = self.font_sheet.get_at(x_coord, 0)
            if color:
                continue