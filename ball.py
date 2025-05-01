import commons
import vector
import images
import pygame

from vector import Vector
from enums import BallType
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, position, velocity=Vector(0, 0), radius=8, 
                 ball_type=BallType.DEFAULT, image: pygame.Surface = None):
        super().__init__()
        
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)
        self.radius = radius
        self.diameter = radius * 2.0

        self.ball_type = BallType(ball_type)

        self.image = image
        if self.image is None:
            self.image = images.default_ball
            
        self.rect = self.image.get_rect(center=self.position.make_int_tuple())
        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True
    
    def update(self):
        self.velocity.y += commons.dT * commons.gravity
        self.position += self.velocity * commons.dT

        self.check_screen_collisions()

        self.rect.center = self.position.make_int_tuple()

    def check_screen_collisions(self):
        if self.position.x < self.radius or self.position.x > commons.screen_w - self.radius:
            self.velocity.x = -self.velocity.x
        if self.position.y < self.radius:
            self.velocity.y = -self.velocity.y
        elif self.position.y > commons.screen_h + self.radius:
            self.kill()