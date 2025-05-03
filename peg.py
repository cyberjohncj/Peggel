### THIRD-PARTY LIBRARIES
import pygame

### LOCAL
import vector
import images

from vector import Vector
from enums import PegType
from pygame.locals import *

PEG_COLORS = {
    PegType.BLUE: (0, 0, 150),
    PegType.ORANGE: (60, 0, 0),
    PegType.GREEN: (0, 60, 0),
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
        
        self.current_peg_type = self.peg_type
        
        # Set base image (untinted)
        self.base_image = image if image is not None else images.default_ball
        self.image = self.base_image.copy()
        self.update_tint()

        self.rect = self.image.get_rect(center=self.position.make_int_tuple())
        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True
        self.hit_at = None
        self.peg_glowing = False
    
    def update(self):
        if self.peg_type != self.current_peg_type:
            self.current_peg_type = self.peg_type

            print("[Console]: Changed color of Peg")
            self.update_tint()

        #self.velocity.y += commons.dT * commons.gravity
        #self.position += self.velocity * commons.dT

        if not self.alive and not self.peg_glowing:
            # Glow
            self.base_image = images.glowing_ball.copy()
            self.update_tint()
            self.rect = self.image.get_rect(center=self.position.make_int_tuple())
            self.image_swapped = True

    def update_tint(self):
        self.image = self.base_image.copy()
        tint_color = PEG_COLORS[self.peg_type]
        self.image.fill(tint_color + (0,), special_flags=pygame.BLEND_RGBA_ADD)

    """
    def check_screen_collisions(self):
        pass
    """