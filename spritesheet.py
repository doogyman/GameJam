from globals import *
import numpy as np
        
def get_sprite(sheet, frame, w, h, r, g, b, scale):
    rect = pygame.Rect((frame * w, 0, w, h))
    sprite = pygame.Surface([w, h], pygame.SRCALPHA)
    rgb_color = np.array([r, g, b])
    sprite.set_colorkey(rgb_color)
    sprite.blit(sheet, (0, 0), rect)
    image = pygame.transform.scale(sprite, (w * scale, h * scale))
    return image
