### STANDARD LIBRARIES
import os
from random import choice

### THIRD-PARTY LIBRARIES
import pygame

backgrounds = []
folder_path = "resources/images/backgrounds/"
for file in os.listdir(folder_path):
    if file.endswith(('.png', '.jpg')):  # fix: use a tuple for endswith
        backgrounds.append(pygame.image.load(os.path.join(folder_path, file)))

test_background = pygame.image.load("resources/images/backgrounds/bliss.png")

# Ball class images
default_ball = pygame.image.load("resources/images/balls/main.png")
glowing_ball = pygame.image.load("resources/images/balls/glow.png")

def get_random_background():
    random_background = choice(backgrounds)
    if random_background:
        return random_background
    return None