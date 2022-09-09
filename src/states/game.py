from typing import List
import pygame
from enum import Enum
from random import randint
from components.text import Text
from globals import ALIGN_CENTER, SIZE_H1, WIN_HEIGHT, WIN_WIDTH

from objects.asteroid import Asteroid
from objects.player import Player

class Game:
    class State(Enum):
        MENU = 0
        PAUSED = 1
        RUNNING = 2
        ENDED = 3

    def __init__(self):
        self.level = 1
        self.state = self.State.MENU
        self.player = None
        self.asteroids : List[Asteroid] = []

    def change_game_state(self, state):
        self.state = state

    def draw(self, win, faded, dt):
        if faded:
            text = Text("PAUSED", 0, WIN_HEIGHT * 0.4, font_size= SIZE_H1, text_align= ALIGN_CENTER)
            text.draw(win, dt)

    def start_new_game(self):
        self.change_game_state(self.State.RUNNING)

        self.asteroids = []
        x = randint(0, WIN_WIDTH)
        y = randint(0, WIN_HEIGHT)

        self.asteroids.append(Asteroid(x, y, level = self.level))

        self.player = Player()

    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))