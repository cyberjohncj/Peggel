### THIRD-PARTY LIBRARIES
import pygame

### LOCAL
from ball import Ball
from peg import Peg

balls = pygame.sprite.Group()
pegs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

def add_ball(ball):
    balls.add(ball)
    all_sprites.add(ball)

def add_peg(peg):
    pegs.add(peg)
    all_sprites.add(peg)

def update_all():
    all_sprites.update()

def draw_all(surface):
    #surface.blit  # if needed
    all_sprites.draw(surface)