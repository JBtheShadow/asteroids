import pygame

from components.button import Button
from components.sfx import Sfx, SoundMode
import components.sfx as s
from globals import ALIGN_CENTER, SIZE_H3, WIN_HEIGHT, WIN_WIDTH
from states.game import Game

NEW_GAME = "new_game"
SETTINGS = "settings"
QUIT = "quit"

class Menu:
    def __init__(self, game: Game, sfx: Sfx):
        self.sfx = sfx
        self.game = game
        self.focused = ''

        self.buttons = {
            NEW_GAME: Button("New Game", WIN_WIDTH / 3, WIN_HEIGHT * 0.25,
                func= (lambda: game.start_new_game()),
                width= WIN_WIDTH / 3,
                height= 50,
                text_align= ALIGN_CENTER,
                font_size= SIZE_H3
            ),
            SETTINGS: Button("Settings", WIN_WIDTH / 3, WIN_HEIGHT * 0.4,
                func= None,
                width= WIN_WIDTH / 3,
                height= 50,
                text_align= ALIGN_CENTER,
                font_size= SIZE_H3
            ),
            QUIT: Button("Quit", WIN_WIDTH / 3, WIN_HEIGHT * 0.55,
                func= (lambda: game.quit_game()),
                width= WIN_WIDTH / 3,
                height= 50,
                text_align= ALIGN_CENTER,
                font_size= SIZE_H3
            ),
        }
    
    def draw(self, win, mouse_xy, mouse_radius, dt):
        for _, button in self.buttons.items():
            button.draw(win, mouse_xy, mouse_radius, dt)

    def run(self, mouse_xy, mouse_radius, clicked):
        for name, button in self.buttons.items():
            if button.check_hover(mouse_xy, mouse_radius):
                self.sfx.play_sfx(s.SELECT, SoundMode.SINGLE)

                if clicked:
                    button.click()
                
                self.focused = name
                break
            elif self.focused == name:
                self.sfx.fx_played = False

    # def click(self, mouse_xy, mouse_radius):
    #     for button in self.buttons:
    #         if button.check_hover(mouse_xy, mouse_radius):
    #             button.click()
    #             break
