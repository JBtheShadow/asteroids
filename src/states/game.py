from typing import List
import pygame
from enum import Enum
from random import randint
from components.sfx import Sfx
from components.text import Text
from globals import ALIGN_CENTER, ALIGN_RIGHT, SIZE_H1, SIZE_H2, SIZE_H4, SIZE_H5, WIN_HEIGHT, WIN_WIDTH

from objects.asteroid import Asteroid
from objects.player import Player
from utils import get_distance

class Game:
    class State(Enum):
        MENU = 0
        PAUSED = 1
        RUNNING = 2
        ENDED = 3

    def __init__(self, sfx: Sfx, save_data: dict = {}):
        self.level = 1
        self.state = self.State.MENU
        self.player = None
        self.asteroids : List[Asteroid] = []
        self.high_score = save_data.get("highScore", 0)
        self.score = 0
        self.screen_text = []
        self.show_game_over = False
        self.sfx = sfx

    def game_over(self):
        self.screen_text = [
            Text(
                "GAME OVER",
                0,
                WIN_HEIGHT * 0.4,
                font_size= SIZE_H1,
                text_align= ALIGN_CENTER,
                fade_in= True,
                fade_out= True
            )
        ]
        self.show_game_over = True

    def change_game_state(self, state):
        self.state = state
        if self.state == self.State.ENDED:
            self.game_over()

    def draw_scores(self, win, dt):
        color = (150, 150, 150)
        Text(f"SCORE: {self.score}", -10, 10, font_size= SIZE_H4, text_align= ALIGN_RIGHT, color= color).draw(win, dt)

        color = (128, 128, 128)
        Text(f"HIGH SCORE: {self.high_score}", 0, 10, font_size= SIZE_H5, text_align= ALIGN_CENTER, color= color).draw(win, dt)

    def draw_paused(self, win, dt):
        Text("PAUSED", 0, WIN_HEIGHT * 0.4, font_size= SIZE_H1, text_align= ALIGN_CENTER).draw(win, dt)

    def draw_screen_text(self, win, dt):
        to_remove = []
        for text in self.screen_text:
            if not text.draw(win, dt):
                to_remove.append(text)
        
        for text in to_remove:
            self.screen_text.remove(text)

        if self.show_game_over and not len(self.screen_text):
            self.show_game_over = False

    def set_level(self, level):
        self.level = level
        self.asteroids = []
        self.spawn_asteroids()

        self.screen_text = [
            Text(
                f"Level {self.level}",
                0,
                WIN_HEIGHT * 0.4,
                font_size= SIZE_H2,
                text_align= ALIGN_CENTER,
                fade_in= True,
                fade_out= True
            )
        ]

        self.player.make_invulnerable()

    def get_pos_away_from_player(self):
        while True:
            x = randint(0, WIN_WIDTH)
            y = randint(0, WIN_HEIGHT)
            if get_distance(x, y, self.player.x, self.player.y) > 200:
                return x, y

    def spawn_asteroids(self):
        for _ in range(self.level):
            x, y = self.get_pos_away_from_player()
            self.asteroids.append(Asteroid(self.sfx, x, y, level = self.level))

    def start_new_game(self):
        self.score = 0
        self.change_game_state(self.State.RUNNING)

        self.player = Player(self.sfx)

        self.set_level(1)

    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))