import commons
import vector
import images
import pygame
import entities

from vector import Vector
from enums import PegType
from pygame.locals import *

PEG_COLORS = {
    PegType.BLUE: (0, 0, 150),
    PegType.ORANGE: (60, 0, 0),
    PegType.GREEN: (0, 255, 0),
    PegType.PURPLE: (128, 0, 128),
}

class Peg(pygame.sprite.Sprite):
    def __init__(self, position, velocity=Vector(0, 0), radius=8, 
                 peg_type=PegType.BLUE, image: pygame.Surface = None):
        super().__init__()
        
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)
        self.radius = radius
        self.diameter = radius * 2.0
        
        if isinstance(peg_type, PegType):
            self.peg_type = peg_type
        elif isinstance(peg_type, int):
            self.peg_type = PegType(peg_type)
        else:
            self.peg_type = PegType.BLUE  # Default
        
        if image is None:
            image = images.default_ball
        tint_color = PEG_COLORS[self.peg_type]
        self.image = image.copy()
        self.image.fill(tint_color + (0,), special_flags=pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect(center=self.position.make_int_tuple())
        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True
        self.dead_since = None
    
    def update(self):
        #self.velocity.y += commons.dT * commons.gravity
        #self.position += self.velocity * commons.dT

        if not self.alive:
            if not entities.balls:
                self.kill()
                return
            
            if not self.dead_since:
                self.dead_since = pygame.time.get_ticks() 
            else:
                elapsed = (pygame.time.get_ticks() - self.dead_since) / 1000
                if elapsed >= 5:
                    self.kill()
                    
        #self.check_screen_collisions()

        pass

    """
    def check_screen_collisions(self):
        pass
    """