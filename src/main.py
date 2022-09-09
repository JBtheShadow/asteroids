import pygame
pygame.init()

from typing import List
from objects.asteroid import Asteroid

from states.game import Game
from states.menu import Menu
from components.text import Text

from globals import BLACK, FPS, WHITE, WIN_HEIGHT, WIN_TITLE, WIN_WIDTH
from utils import do_circles_overlap, get_distance
from config import *


win: pygame.Surface
mouse_x: float
mouse_y: float
game: Game
menu: Menu

def load():
    global win, mouse_x, mouse_y, game, menu

    mouse_x, mouse_y = 0, 0

    pygame.mouse.set_visible(False)
    pygame.display.set_caption(WIN_TITLE)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    game = Game()
    menu = Menu(game)

clicked: bool
def mouse_pressed(x, y):
    global clicked
    if game.state == game.State.RUNNING:
        game.player.shoot()
    elif game.state == game.State.MENU:
        menu.click((x, y), 10)
    else:
        clicked = True

def key_pressed(key):
    if game.state == game.State.RUNNING:
        if key in [pygame.K_w, pygame.K_UP, pygame.K_KP8]:
            game.player.thrusting = True
        
        if key in [pygame.K_SPACE, pygame.K_s, pygame.K_DOWN, pygame.K_KP5]:
            game.player.shoot()

        if key in [pygame.K_ESCAPE]:
            game.change_game_state(game.State.PAUSED)

    elif game.state == game.State.PAUSED:
        if key in [pygame.K_ESCAPE]:
            game.change_game_state(game.State.RUNNING)

def key_released(key):
    if not game.state == game.State.MENU:
        if key in [pygame.K_w, pygame.K_UP, pygame.K_KP8]:
            game.player.thrusting = False

def update(dt):
    global mouse_x, mouse_y, clicked
    player = game.player
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if game.state == game.State.RUNNING:
        if not player.move(dt):
            game.change_game_state(game.State.ENDED)
            return

        to_remove : List[Asteroid] = []
        for asteroid in game.asteroids:
            destroyed = False

            if player.status != player.Status.EXPLODING:
                if do_circles_overlap((player.x, player.y), player.radius, (asteroid.x, asteroid.y), asteroid.radius):
                    player.explode()

                    if player.lives > 1 and not destroyed:
                        to_remove.append(asteroid)
                        destroyed = True

            for laser in player.lasers:
                if get_distance(asteroid.x, asteroid.y, laser.x, laser.y) <= asteroid.radius:
                    laser.explode()

                    if player.status != player.Status.EXPLODING and not destroyed:
                        to_remove.append(asteroid)
                        destroyed = True

            if not destroyed:
                asteroid.move(dt)
        
        to_add : List[Asteroid] = []
        for asteroid in to_remove:
            game.asteroids.remove(asteroid)
            to_add = asteroid.spawn_debris()

        for asteroid in to_add:
            game.asteroids.append(asteroid)
    elif game.state == game.State.MENU:
        clicked = False

def draw(dt, fps):
    player = game.player
    faded = game.state == game.State.PAUSED

    if game.state in [game.State.RUNNING, game.State.PAUSED]:
        #change how shapes are drawn. Control opacity from paused state
        #over here, all at once, instead of each individual shape
        game_surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        game_surf.fill(BLACK)

        player.draw_lives(game_surf, show_debugging)
        player.draw(game_surf, dt, show_debugging)

        for asteroid in game.asteroids:
            asteroid.draw(game_surf, show_debugging)

        if faded:
            game_surf.set_alpha(128)

        win.blit(game_surf, (0, 0, WIN_WIDTH, WIN_HEIGHT))

        #Pause text doesn't get the opacity treatment
        game.draw(win, faded, dt)
    elif game.state in [game.State.MENU]:
        menu.draw(win, (mouse_x, mouse_y), 10, dt)

    if not game.state in [game.State.RUNNING]:
        pygame.draw.circle(win, WHITE, (mouse_x, mouse_y), 10)

    if show_fps:
        text = Text(f"{int(fps)} FPS", 10, 10)
        text.draw(win, dt)

should_quit = False
def handle_events():
    global should_quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_quit = True
            break
    
        if event.type == pygame.KEYDOWN:
            key_pressed(event.key)

        if event.type == pygame.KEYUP:
            key_released(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            mouse_pressed(x, y)


def main():
    run = True
    clock = pygame.time.Clock()

    load()

    while run:
        dt = clock.tick(FPS) / 1000
        fps = clock.get_fps()

        handle_events()
        if should_quit:
            run = False
            break

        update(dt)
        win.fill(BLACK)
        draw(dt, fps)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()