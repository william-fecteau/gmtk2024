from typing import Any

TARGET_FPS = 60
TARGET_CUTSCENE_FPS = 50
SCREEN_SIZE = 1280, 720

# Colors
GREEN_COLOR = 0, 146, 32
BLACK = 0, 0, 0
LIGHT_BLACK = 10, 10, 10
EMERALD = 68, 207, 108
LIGHT_GRAY = 125, 125, 125
DARK_GRAY = 46, 46, 46
PURPLE = (255,0,255)
WHITE = (240,240,240)

WORLD_COLORS : dict[int, Any] = {
    0: (5, 173, 22),
    1: (50, 199, 184),
    2: (200,80,230),
    3: (207, 35, 138),
    4: (230, 18, 47),
    5: (95, 131, 222)
}

NB_LEVELS = 10
NB_WORLD = 3
