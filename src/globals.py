import pygame

WIN_TITLE = 'Asteroids'
WIN_WIDTH = 1280
WIN_HEIGHT = 720
FPS = 60

FONT_FAMILY = "Lucida Sans"

SIZE_P = "p"
SIZE_H1 = "h1"
SIZE_H2 = "h2"
SIZE_H3 = "h3"
SIZE_H4 = "h4"
SIZE_H5 = "h5"
SIZE_H6 = "h6"
fonts = {
    SIZE_P: pygame.font.SysFont(FONT_FAMILY, 16),
    SIZE_H1: pygame.font.SysFont(FONT_FAMILY, 60),
    SIZE_H2: pygame.font.SysFont(FONT_FAMILY, 40),
    SIZE_H3: pygame.font.SysFont(FONT_FAMILY, 30),
    SIZE_H4: pygame.font.SysFont(FONT_FAMILY, 20),
    SIZE_H5: pygame.font.SysFont(FONT_FAMILY, 15),
    SIZE_H6: pygame.font.SysFont(FONT_FAMILY, 10),
}

ALIGN_LEFT = "left"
ALIGN_CENTER = "center"
ALIGN_RIGHT = "right"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FADED_RED = (200, 50, 50)
HURT_RED = (200, 0, 0)
WARNING_ORANGE = (200, 128, 0)
RED = (255, 0, 0)
GRAY = (175, 175, 175)
YELLOW1 = (255, 200, 25)
YELLOW2 = (255, 225, 50)
ORANGE = (255, 128, 50)
THRUST_YELLOW = (255, 175, 50)
THRUST_ORANGE = (255, 100, 25)
EXPLOSION_RED = (255, 50, 25)
EXPLOSION_ORANGE = (255, 128, 50)
EXPLOSION_YELLOW = (255, 225, 50)
GREEN = (0, 255, 0)

TEXT_FADE_DUR = 5
SHAPE_WIDTH = 2
DEBUG_WIDTH = 1