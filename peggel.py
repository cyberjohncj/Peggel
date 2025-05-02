import sys

### Local Imports
try:
    import commons
    import pygame
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

    from ball import Ball
    from peg import Peg
except ImportError as e:
    print("[ERROR]: Unable to import local modules.")
    print(str(e.msg))
    sys.exit(1)

def update():
    entities.update_all()

    if not entities.pegs:
        ### Test pegs
        for row in range(0, 3, 1):
            for col in range(0, 5, 1):
                entities.add_peg(Peg(Vector(commons.screen_w / 2 + (col * 90), commons.screen_h / 2 + (row * 90))))
                entities.add_peg(Peg(Vector(commons.screen_w / 2 - (col * 90), commons.screen_h / 2 + (row * 90))))
    else:
        if entities.balls:
            for ball in entities.balls:
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
                        print(ball)
                        #print("Touching")
                        # Touching

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
    
    if not sounds.is_music_playing:
        sounds.play_music("bgm2.mp3", True)

    update()
    draw()

    pygame.display.flip()

    commons.dT = 0.001 * clock.tick(144)

pygame.quit()