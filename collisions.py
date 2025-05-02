import commons
import vector

from vector import Vector
from ball import Ball
from peg import Peg

EPSILON = 0.25
RESTITUITON = 0.90
BOUNCINESS = 1.0

def is_ball_touching_peg(ball: Ball, peg: Peg, dT: float) -> bool:
    samples = commons.collision_sample_size  # Number of points to sample along the ball's path

    # Check starting position
    start_to_peg = vector.copy(ball.previous_position) - peg.position
    if vector.length(start_to_peg) <= (ball.radius + peg.radius - EPSILON):
        return True

    # Check ending position
    end_to_peg = vector.copy(ball.position) - peg.position
    if vector.length(end_to_peg) <= (ball.radius + peg.radius - EPSILON):
        return True

    # Check intermediate points along ball's path
    for i in range(1, samples):
        t = i / samples  # Interpolation fraction

        # Interpolate position between previous and current
        interpolated_pos = vector.copy(ball.previous_position)
        delta = vector.copy(ball.position) - ball.previous_position
        interpolated_pos += delta * t

        # Distance from interpolated point to peg
        distance = vector.copy(interpolated_pos) - peg.position
        if vector.length(distance) <= (ball.radius + peg.radius - EPSILON):
            return True

    return False  # No collision detected

def resolve_collision(ball: Ball, pegs: list[Peg], dt: float) -> Ball:
    tolerance = 1e-3  # Binary search precision
    best_fraction = 1.0  # Tracks earliest collision fraction along ball's path
    best_peg = None
    best_normal = None

    for peg in pegs:
        low, high = 0.0, 1.0
        impact_fraction = None

        # Binary search to find the earliest point of contact along ball's path
        while high - low > tolerance:
            mid = (low + high) / 2.0

            # Interpolate ball's position at 'mid' between previous and current positions
            sample_point = vector.copy(ball.previous_position)
            delta = vector.copy(ball.position) - ball.previous_position
            sample_point += delta * mid

            # Check distance from peg to this interpolated point
            distance = vector.copy(sample_point) - peg.position
            if vector.length(distance) <= (ball.radius + peg.radius - EPSILON):
                impact_fraction = mid  # Collision detected at this fraction
                high = mid  # Search earlier part
            else:
                low = mid  # Search later part

        # If this is the earliest collision so far, store it
        if impact_fraction is not None and impact_fraction < best_fraction:
            best_fraction = impact_fraction
            best_peg = peg

            # Calculate exact collision position
            collision_position = vector.copy(ball.previous_position)
            delta = vector.copy(ball.position) - ball.previous_position
            collision_position += delta * impact_fraction

            # Compute normal vector from peg to collision point
            normal = vector.copy(collision_position) - peg.position
            if vector.length(normal) != 0:
                vector.normalize(normal)
            else:
                normal = Vector(0, -1)  # Fallback normal if exactly centered
            best_normal = normal

    # No collision detected; return unchanged ball
    if best_peg is None or best_normal is None:
        return ball

    # Compute corrected final position of ball after resolving collision
    collision_position = vector.copy(ball.previous_position)
    delta = vector.copy(ball.position) - ball.previous_position
    collision_position += delta * best_fraction

    # Reposition ball to avoid overlap
    final_normal = vector.copy(best_normal) * (ball.radius + best_peg.radius)
    final_position = vector.copy(best_peg.position) + final_normal
    ball.position = final_position

    # Reflect velocity based on collision normal and bounciness
    v_dot_n = ball.velocity.x * best_normal.x + ball.velocity.y * best_normal.y
    bounce = BOUNCINESS

    # Reduce bounce if the ball is moving slowly
    speed = vector.length(ball.velocity)
    if speed < 2:
        bounce *= 0.30
    if speed < 1:
        bounce *= 0.10

    # Only reflect if moving into the surface
    if v_dot_n < 0:
        correction = vector.copy(best_normal) * ((1 + RESTITUITON * bounce) * v_dot_n)
        ball.velocity -= correction

    return ball