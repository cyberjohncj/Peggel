import sys

import pygame

import commons
import config
import states

from states import GameState, MenuState, PlayState, BallState, PegState
from engine import Game

def update():
    if states.game_state == GameState.PLAYING:
        commons.game.update()
    
def draw():
    if states.game_state == GameState.PLAYING:
        commons.game.draw()

pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))
commons.game_screen = pygame.Surface((commons.game_screen_w, commons.screen_h))

pygame.display.set_caption("Peggel")

# Game Variables
can_clear = False
commons.game = Game()

commons.dT = 0.0
clock = pygame.time.Clock()
mouse_position = (0, 0)

states.game_state = GameState.PLAYING

# Main Loop
while commons.game.game_running:
    mouse_position = pygame.mouse.get_pos()

    commons.game.handle_events()

    update()
    draw()

    pygame.display.flip()

    commons.dT = 0.001 * clock.tick(144)

pygame.quit()