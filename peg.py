import commons
import vector
import images
import pygame

from vector import Vector
from enum import Enum
from pygame.locals import *

class PegType(Enum):
    BLUE = 0
    ORANGE = 1
    GREEN = 2
    PURPLE = 3

class Peg(pygame.sprite.Sprite):
    def __init__(self, position, velocity=Vector(0, 0), radius=8, 
                 peg_type=PegType.BLUE, image: pygame.Surface = None):
        super().__init__()
        
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)

        self.radius = radius
        self.diameter = radius * 2.0

        self.peg_type = PegType(peg_type)

        self.image = image
        if self.image is None:
            self.image = images.default_ball
        self.rect = self.image.get_rect(center=self.position.make_int_tuple())

        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True
    
    def update(self):
        #self.velocity.y += commons.dT * commons.gravity
        #self.position += self.velocity * commons.dT

        #self.check_screen_collisions()

        pass

    def check_screen_collisions(self):
        pass