import pygame

from peg import Peg

class Rect:    
    def __init__(self, x, y, w, h):
        self.x = x  # Center x-coordinate
        self.y = y  # Center y-coordinate
        self.w = w  # Half-width
        self.h = h  # Half-height

    def contains_peg(self, peg: Peg) -> bool:
        return (self.x - self.w <= peg.position.x < self.x + self.w and
                self.y - self.h <= peg.position.y < self.y + self.h)

    def intersects(self, other: 'Rect') -> bool:
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)

class QuadtreePegs:    
    def __init__(self, boundary: Rect, num_pegs: int):
        self.boundary = boundary  # Bounding rectangle of this node
        self.capacity = max(num_pegs // 4, 4)  # Minimum capacity of 4
        self.pegs: list[Peg] = []  # Pegs in this node
        self.divided = False  # Whether this node has been subdivided

    def subdivide(self):
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.w / 2, self.boundary.h / 2

        # Create four child Rects
        ne = Rect(x + w, y - h, w, h)
        nw = Rect(x - w, y - h, w, h)
        se = Rect(x + w, y + h, w, h)
        sw = Rect(x - w, y + h, w, h)

        # Assign new Quadtree nodes to each quadrant
        self.northeast = QuadtreePegs(ne, self.capacity)
        self.northwest = QuadtreePegs(nw, self.capacity)
        self.southeast = QuadtreePegs(se, self.capacity)
        self.southwest = QuadtreePegs(sw, self.capacity)
        self.divided = True

    def insert(self, peg: Peg) -> bool:
        if not self.boundary.contains_peg(peg):
            return False  # Peg is out of bounds

        if len(self.pegs) < self.capacity:
            self.pegs.append(peg)
            return True
        else:
            if not self.divided:
                self.subdivide()

            # Try inserting into child quadrants
            return (self.northeast.insert(peg) or
                    self.northwest.insert(peg) or
                    self.southeast.insert(peg) or
                    self.southwest.insert(peg))

    def show(self, surface):
        rect = pygame.Rect(
            self.boundary.x - self.boundary.w,
            self.boundary.y - self.boundary.h,
            self.boundary.w * 2,
            self.boundary.h * 2
        )
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)  # White outline

        # Recursively draw children
        if self.divided:
            self.northeast.show(surface)
            self.northwest.show(surface)
            self.southeast.show(surface)
            self.southwest.show(surface)

    def query(self, range: Rect) -> list[Peg]:
        found = []

        if not self.boundary.intersects(range):
            return found  # No overlap, skip this node

        # Check pegs in this node
        for peg in self.pegs:
            if range.contains_peg(peg):
                found.append(peg)

        # Check children if subdivided
        if self.divided:
            found.extend(self.northeast.query(range))
            found.extend(self.northwest.query(range))
            found.extend(self.southeast.query(range))
            found.extend(self.southwest.query(range))

        return found