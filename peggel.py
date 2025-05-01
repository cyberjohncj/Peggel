import commons
import pygame
import vector
import states
import entities
import images

from vector import Vector
from states import GameState, MenuState, PlayState
from enums import BallType, PegType
from ball import Ball
from peg import Peg

def update():
    entities.update_all()

def draw():
    commons.screen.fill((50, 50, 50))
    commons.screen.blit(images.test_background, (0, 0))
    entities.draw_all(commons.screen)

pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))

pygame.display.set_caption("Peggel")

app_running = True
commons.dT = 0.0
clock = pygame.time.Clock()
mouse_position = (0, 0)

# test peg
entities.add_peg(Peg(Vector(commons.screen_w / 2, commons.screen_h / 2)))
# test orange peg
entities.add_peg(Peg(Vector(commons.screen_w / 2 + 50, commons.screen_h / 2), peg_type=PegType.ORANGE))

while app_running:
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                     ball = Ball(Vector(event.pos[0], event.pos[1]), vector.random_vector() * 150)
                     entities.add_ball(ball)

    update()
    draw()

    pygame.display.flip()

    commons.dT = 0.001 * clock.tick(144)

pygame.quit()