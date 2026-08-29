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

# This function basically takes part of an image an ouptuts it, this is differnet to spritehsheet as it does not blit directly, can alsso be clipped multiple times

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy