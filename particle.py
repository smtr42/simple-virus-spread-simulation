import math
import random


def add_vectors(vector1, vector2):
    """ This add two vectors. Angle is in radian.

    Args:
        vector1(tuple): first vector
        vector2(tuple): second vector
    returns:
        angle, length (tuple): resulted vector
    """

    angle1, length1 = vector1
    angle2, length2 = vector2
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return angle, length


def collide(p1, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce
        i.e. update their angle, speed and position """

    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:

        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        angle1speed1 = p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass
        anglespeed2 = angle, 2 * p2.speed * p2.mass / total_mass
        (p1.angle, p1.speed) = add_vectors(angle1speed1, anglespeed2)

        angle2speed2 = p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass
        anglespeed1 = angle + math.pi, 2 * p1.speed * p1.mass / total_mass
        (p2.angle, p2.speed) = add_vectors(angle2speed2, anglespeed1)

        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap
        return True


def contamination(p1, p2):
    if p1.state == 1 or p2.state == 1:
        p1.colour = (255, 0, 0)
        p2.state = 1
        p1.state = 1
        p2.colour = (255, 0, 0)


def heal_from_time(elapsed_time, dt, particle):
    if particle.state == 1:
        particle.time_from_contamination += dt
    if particle.time_from_contamination >= 5.0:
        particle.colour = (0, 255, 0)
        particle.state = 2


class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, xy, size, state, mass=1, ):
        self.x, self.y = xy
        self.size = size
        self.colour = (0, 0, 255)
        self.sick_colour = (255, 0, 0)
        self.heal_colour = (0, 255, 0)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1  # 1
        self.elasticity = 1  # 0.9
        self.state = state
        self.time_from_contamination = 0

    def move(self):
        """ Update position based on speed, angle
            Update speed based on drag """

        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag
        # if self.speed > 0.1:
        #     self.speed = 0.1


class Simulation:
    """ Defines the boundary of a simulation and its properties """

    def __init__(self, screen_dimensions):
        self.width, self.height = screen_dimensions
        self.particles = []
        self.colour = (255, 255, 255)
        self.mass_of_air = 0.0  # 0.2
        self.elasticity = 1  # 0.75
        self.acceleration = None

    def add_particle(self, n=1, **kargs):
        """ Add n particles with properties given by keyword arguments """
        for i in range(n):
            # size = kargs.get('size', random.randint(10, 20))
            # mass = kargs.get('mass', random.randint(100, 10000))
            size = 10
            mass = 100
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))
            if i != 1:
                state = 0
            else:
                state = 1
            particle = Particle((x, y), size, state, mass)
            # particle.speed = kargs.get('speed', random.random())
            particle.speed = 1
            particle.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            if state == 1:
                particle.colour = kargs.get('colour', (255, 0, 0))
            else:
                particle.colour = kargs.get('colour', (0, 0, 255))
            particle.drag = (particle.mass / (
                    particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)

    def update(self, elapsed_time, dt):
        """  Moves particles and tests for collisions with the walls and each other """

        for i, particle in enumerate(self.particles):
            particle.move()
            self.wall_bounce(particle)
            for particle2 in self.particles[i + 1:]:
                if collide(particle, particle2):
                    contamination(particle, particle2)
            heal_from_time(elapsed_time, dt, particle)

    def wall_bounce(self, particle):
        """ Tests whether a particle has hit the boundary of the environment """

        if particle.x > self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity
