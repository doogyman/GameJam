from globals import *
import numpy as np
from pathlib import Path
def load_image(sheet: Path, r, g, b):
    rgb_color = np.array([r, g, b])
    image = pygame.image.load(str(sheet)).convert_alpha()
    image: pygame.Surface = image.set_colorkey(rgb_color)
    return image

