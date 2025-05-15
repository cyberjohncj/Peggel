### THIRD-PARTY LIBRARIES
import pygame

### LOCAL
import commons
import config # TODO
import vector
import states
import entities
import images # TODO
import sounds

from vector import Vector
from states import GameState, MenuState, PlayState, BallState, PegState
from enums import BallType, PegType
from collisions import is_ball_touching_peg, resolve_collision
from quadtree import QuadtreePegs, Rect
from etc import add_peg, change_peg_colors
from ball import Ball
from peg import Peg

class Game:
    def __init__(self):
        self.game_running = True
        self.mouse_1 = None
        self.mouse_2 = None
        self.can_clear = False
        self.track_stopped = False

        self.background = None

        # Initialize the quadtree boundary (center_x, center_y, half_width, half_height)
        self.boundary = Rect(
            commons.game_screen_w / 2,
            commons.screen_h / 2,
            commons.game_screen_w / 2,
            commons.screen_h / 2
        )

        # Create the quadtree with a default capacity (e.g., 4)
        self.quad_tree = QuadtreePegs(self.boundary, 4)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_running = False
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_1 = event.pos
            elif pygame.mouse.get_pressed()[2]: ### This checks whether the second mouse button is being held down.
                self.mouse_2 = event.pos
                """
                if states.game_state == states.GameState.LEVEL_EDITING:
                    mouse_x_in_game = mouse_position[0] - commons.game_x
                    
                    if 0 <= mouse_x_in_game < commons.game_screen_w:
                        mouse_peg = Peg(Vector(mouse_x_in_game, event.pos[1]))
                        if not pygame.sprite.spritecollide(mouse_peg, entities.pegs, False):
                            add_peg(Vector(mouse_x_in_game, event.pos[1]))

                            print("[Console]: Spawned a Peg")
                            print("[Console] Ran rebuild_quad_tree()")
                            rebuild_quad_tree()
                """

    def update(self):
        if states.game_state == GameState.PLAYING:
            ### Local Variables
            peg_killed_this_frame = False

            if not self.background:
                self.background = (images.get_random_background() or images.test_background)

            if self.mouse_1: ### Check if the mouse was pressed for this frame.
                mouse_x_in_game = self.mouse_1[0] - commons.game_x
                if 0 <= mouse_x_in_game < commons.game_screen_w:
                    if not entities.balls:
                        velocity = (Vector(mouse_x_in_game, self.mouse_1[1]) - Vector(commons.x_centered, 10)) * 1.5
                        ball = Ball(Vector(commons.x_centered, 10), velocity)
                        entities.add_ball(ball)
                        sounds.cannon_shot.play()
                        
                self.mouse_1 = None
            
            if self.mouse_2: ### TODO
                self.mouse_2 = None
                pass

            ### Handle Updates
            entities.update_all()

            if entities.balls:
                # Since there is a ball, the screen can be cleared.
                self.can_clear = True

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
                    
                    nearby_pegs = self.quad_tree.query(query_rect)

                    for peg in nearby_pegs:
                        ball_touching_peg = is_ball_touching_peg(ball, peg, commons.dT)
                        if ball_touching_peg:
                            ball.state = BallState.ACTIVE
                            ball = resolve_collision(ball, nearby_pegs, commons.dT)

                            if peg.alive:
                                peg.alive = False
                                peg.hit_at = pygame.time.get_ticks()

                                ### Play a Sound
                                sounds.peghit1.play()

            elif self.can_clear: ### There are no balls, so if can_clear is true, we will just clear the screen now.
                self.can_clear = False

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
                    self.rebuild_quad_tree()
            elif config.use_test_grid: ### There are no pegs alive, and the game has been configured to automatically spawn a test grid.
                commons.total_pegs = 0

                for row in range(0, 6):
                    for col in range(1, 5):
                        x_offset = col * 50
                        y = commons.screen_h / 2 + row * 50

                        x_right = commons.game_screen_w / 2 + x_offset
                        add_peg(Vector(x_right, y))

                        x_left = commons.game_screen_w / 2 - x_offset
                        add_peg(Vector(x_left, y))

                    add_peg(Vector(commons.game_screen_w / 2, commons.screen_h / 2 + row * 50))
                
                change_peg_colors()

                print("[Console]: Ran rebuild_quad_tree()")
                self.rebuild_quad_tree()

            if not sounds.track_is_playing and not self.track_stopped:
                played_track = sounds.play_random_track()
                if not played_track:
                    print("[Console]: Failed to get a random track.")
                    self.track_stopped = True ### Disable track

    def draw(self):
        commons.screen.fill((25, 25, 25))
        commons.game_screen.fill((255, 255, 255))

        commons.game_screen.blit(self.background, (0, 0))

        entities.draw_all(commons.game_screen)

        # Center game screen on the main display
        commons.screen.blit(commons.game_screen, (commons.game_x, 0))


    def rebuild_quad_tree(self):
        self.quad_tree = QuadtreePegs(self.boundary, len(entities.pegs))
        for peg in entities.pegs:
            self.quad_tree.insert(peg)