### STANDARD LIBRARIES
import sys

### THIRD-PARTY LIBRARIES
import pygame

### LOCAL
import commons
import config
import vector
import states
import entities
import images
import sounds

from vector import Vector
from states import GameState, MenuState, PlayState
from enums import BallType, PegType
from collisions import is_ball_touching_peg, resolve_collision
from quadtree import QuadtreePegs, Rect
from etc import add_peg, change_peg_colors
from ball import Ball
from peg import Peg

### SETTINGS
use_test_grid = True

def rebuild_quad_tree():
    global quad_tree
    
    quad_tree = QuadtreePegs(boundary, len(entities.pegs))
    for peg in entities.pegs:
        quad_tree.insert(peg)

def update():
    global can_clear

    ### Local Variables
    peg_killed_this_frame = False

    entities.update_all()

    if not entities.pegs and use_test_grid:
        commons.total_pegs = 0

        for row in range(0, 5):
            for col in range(1, 7):
                x_offset = col * 60
                y = commons.screen_h / 2 + row * 60

                x_right = commons.screen_w / 2 + x_offset
                add_peg(Vector(x_right, y))

                x_left = commons.screen_w / 2 - x_offset
                add_peg(Vector(x_left, y))

            add_peg(Vector(commons.screen_w / 2, commons.screen_h / 2 + row * 60))
        
        change_peg_colors()

        print("[Console]: Ran rebuild_quad_tree()")
        rebuild_quad_tree()

    if entities.balls:
        # Since there is a ball, the screen can be cleared.
        can_clear = True

        ### Ball Loop
        for ball in entities.balls:
            #print(ball.position.x, ball.position.y)
            """
            pegs_hit = pygame.sprite.spritecollide(ball, entities.pegs, False)
            # TODO Implement "Quadtree" Goal: Have a list of pegs that are in the same area of the screen as the ball.
            if pegs_hit:
                for peg in pegs_hit:
                    if is_ball_touching_peg(ball, peg, commons.dT):
                        print("Hit")
            """

            ### Get Pegs
            query_rect = Rect(ball.position.x, ball.position.y, commons.query_rect_size, commons.query_rect_size)
            
            nearby_pegs = quad_tree.query(query_rect)

            for peg in nearby_pegs:
                ball_touching_peg = is_ball_touching_peg(ball, peg, commons.dT)
                if ball_touching_peg:
                    ball = resolve_collision(ball, nearby_pegs, commons.dT)

                    if peg.alive:
                        peg.alive = False
                        peg.hit_at = pygame.time.get_ticks()

                        ### Play a Sound
                        sounds.peghit1.play()

    elif can_clear: # There are no balls, so if can_clear is true, we will just clear the screen now.
        can_clear = False

        print("[Console]: Cleaning up Pegs")

        for peg in entities.pegs:
            if not peg.alive:
                peg.kill()
                peg_killed_this_frame = True
                commons.total_pegs -= 1

        #rebuild_quad_tree()

    if entities.pegs:
        for peg in entities.pegs:
            if peg.hit_at and not peg.alive:
                ### If a Peg has been dead for 5 seconds without being killed, it will just automatically be killed.
                if ((pygame.time.get_ticks() - peg.hit_at) / 1000 >= 5):
                    peg.kill()
                    peg_killed_this_frame = True
                    commons.total_pegs -= 1

        ### Since there are still pegs, and a peg was killed in this frame/update, we will rebuild the quad tree.
        if peg_killed_this_frame:
            print("[Console]: Ran rebuild_quad_tree()")
            rebuild_quad_tree()
      

def draw():
    commons.screen.fill((50, 50, 50))
    commons.screen.blit(images.test_background, (0, 0))
    entities.draw_all(commons.screen)

pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))

pygame.display.set_caption("Peggel")

### Game Variables
done = False
can_clear = False

app_running = True
commons.dT = 0.0
clock = pygame.time.Clock()
mouse_position = (0, 0)

# test orange peg
#entities.add_peg(Peg(Vector(commons.screen_w / 2 + 50, commons.screen_h / 2), peg_type=PegType.ORANGE))

### Quadtree implementation
boundary = Rect(commons.screen_w / 2, commons.screen_h / 2, commons.screen_w / 2, commons.screen_h / 2)
quad_tree = QuadtreePegs(boundary, 4)
query_rect = Rect(0, 0, 0, 0)
nearby_pegs = []

### Main Loop ###
while app_running:
    mouse_position = pygame.mouse.get_pos()

    ### Add pegs to quadtree
    if quad_tree.pegs == [] and entities.pegs:
        for peg in entities.pegs:
            quad_tree.insert(peg)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not entities.balls and event.button == pygame.BUTTON_LEFT:
                     ball = Ball(Vector(event.pos[0], 10))
                     entities.add_ball(ball)
                     sounds.cannon_shot.play()
            elif event.button == pygame.BUTTON_MIDDLE:
                ### Adding a Peg
                add_peg(Vector(event.pos[0], event.pos[1]))

                print("[Console]: Spawned a Peg")
                print("[Console] Ran rebuild_quad_tree()")
                rebuild_quad_tree()
    
    if not sounds.is_music_playing:
        sounds.play_music("bgm2.mp3", True)

    update()
    draw()

    pygame.display.flip()

    commons.dT = 0.001 * clock.tick(144)

pygame.quit()