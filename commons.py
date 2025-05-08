screen_w = 960
screen_h = 720

game_screen_w = screen_w // 1.5
# game height = screen height

x_centered = game_screen_w // 2
game_x = (screen_w - game_screen_w) // 2 # Centered

total_pegs = 0

orange_pegs = 0
green_pegs = 0
purple_pegs = 0

dT = 0.0
gravity = 400 # 650

collision_sample_size = 10

ball_radius, peg_radius = 8, 14

query_rect_size = ball_radius*1.2 + peg_radius*1.2

screen = None
game_screen = None