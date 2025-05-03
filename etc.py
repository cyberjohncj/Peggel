### STANDARD LIBRARIES
from random import shuffle

### LOCAL
import commons
import config
import entities

from vector import Vector
from enums import PegType
from peg import Peg

def add_peg(position: Vector):
    if commons.total_pegs >= config.max_total_pegs:
        return

    entities.add_peg(Peg(position, peg_type=PegType.BLUE))
    commons.total_pegs += 1

    #change_peg_colors()

def change_peg_colors(color_map: list = None):
    peg_list = list(entities.pegs.sprites())

    if color_map:
        pass # Not Implemented
    else:
        target_oranges = config.max_orange_pegs
        target_greens = config.max_green_pegs

        if len(entities.pegs) < config.max_orange_pegs:
            print(f"[Console Warning]: Level has less than {str(config.max_orange_pegs)} pegs.")

            target_oranges = 1 if len(entities.pegs) <= 3 else len(entities.pegs) - 2

            if len(entities.pegs) <= 2:
                target_greens = len(entities.pegs) - target_oranges

        for peg in peg_list:
            peg.peg_type = PegType.BLUE

        shuffle(peg_list)

        for i in range(min(target_oranges, len(peg_list))):
            p = peg_list[i]
            p.peg_type = PegType.ORANGE

        for i in range(target_oranges, min(target_oranges + target_greens, len(peg_list))):
            p = peg_list[i]
            p.peg_type = PegType.GREEN