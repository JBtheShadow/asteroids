import pygame

from components.button import Button
from globals import ALIGN_CENTER, SIZE_H3, WIN_HEIGHT, WIN_WIDTH
from states.game import Game


class Menu:
    def __init__(self, game: Game):
        self.game = game

        self.buttons = [
            Button("New Game", WIN_WIDTH / 3, WIN_HEIGHT * 0.25,
                func= (lambda: game.start_new_game()),
                width= WIN_WIDTH / 3,
                height= 50,
                text_align= ALIGN_CENTER,
                font_size= SIZE_H3
            ),
            Button("Settings", WIN_WIDTH / 3, WIN_HEIGHT * 0.4,
                func= None,
                width= WIN_WIDTH / 3,
                height= 50,
                text_align= ALIGN_CENTER,
                font_size= SIZE_H3
            ),
            Button("Quit", WIN_WIDTH / 3, WIN_HEIGHT * 0.55,
                func= (lambda: game.quit_game()),
                width= WIN_WIDTH / 3,
                height= 50,
                text_align= ALIGN_CENTER,
                font_size= SIZE_H3
            ),
        ]
    
    def draw(self, win, mouse_xy, mouse_radius, dt):
        for button in self.buttons:
            button.draw(win, mouse_xy, mouse_radius, dt)

    def click(self, mouse_xy, mouse_radius):
        for button in self.buttons:
            if button.check_hover(mouse_xy, mouse_radius):
                button.click()
                break
