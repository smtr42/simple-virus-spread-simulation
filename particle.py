import math
import random


def addVectors(angle1length1, angle2length2):
    angle1, length1 = angle1length1
    angle2, length2 = angle2length2
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
        (p1.angle, p1.speed) = addVectors(angle1speed1, anglespeed2)
        angle2speed2 = p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass
        anglespeed1 = angle + math.pi, 2 * p1.speed * p1.mass / total_mass
        (p2.angle, p2.speed) = addVectors(angle2speed2, anglespeed1)

        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap
        if p1.state:
            p2.state = 1
            p2.colour = (255, 0, 0)
        elif p2.state:
            p1.state = 1
            p1.colour = (255, 0, 0)


class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, xy, size, state, mass=1, ):
        self.x, self.y = xy
        self.size = size
        self.colour = (0, 0, 255)
        self.sick_colour = (255, 0, 0)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1  # 1
        self.elasticity = 1  # 0.9
        self.state = state

    def move(self):
        """ Update position based on speed, angle
            Update speed based on drag """

        # (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag
        if self.speed > 0.1:
            self.speed = 0.1

    def mouseMove(self, pos):
        """ Change angle and speed to move towards a given point """
        x, y = pos
        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5 * math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1


class Environment:
    """ Defines the boundary of a simulation and its properties """

    def __init__(self, wh):
        self.width, self.height = wh
        self.particles = []
        self.colour = (255, 255, 255)
        self.mass_of_air = 0.0  # 0.2
        self.elasticity = 1  # 0.75
        self.acceleration = None

    def addParticles(self, n=1, **kargs):
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
            particle.colour = kargs.get('colour', (0, 0, 255))
            particle.drag = (particle.mass / (
                    particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)
            print(self.particles)

    def update(self):
        """  Moves particles and tests for collisions with the walls and each other """

        for i, particle in enumerate(self.particles):
            particle.move()
            if self.acceleration:
                particle.accelerate(self.acceleration)
            self.bounce(particle)
            for particle2 in self.particles[i + 1:]:
                collide(particle, particle2)

    def bounce(self, particle):
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

    def findParticle(self, pos):
        """ Returns any particle that occupies position x, y """
        x, y = pos
        for particle in self.particles:
            if math.hypot(particle.x - x, particle.y - y) <= particle.size:
                return particle
        return None
