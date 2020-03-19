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
    """ Tests if two particles collide
    Args:
        p1(obj): first particle
        p2(obj): second particle
    returns:
        True (bool): notify the collide has happened
        """

    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        if p1.speed == 0:
            p1_speed = p2.speed
        else:
            p1_speed = p1.speed
        if p2.speed == 0:
            p2_speed = p1.speed
        else:
            p2_speed = p2.speed

        angle1speed1 = p1.angle, p1_speed * (p1.mass - p2.mass) / total_mass
        anglespeed2 = angle, 2 * p2_speed * p2.mass / total_mass
        (p1.angle, p1.speed) = add_vectors(angle1speed1, anglespeed2)

        angle2speed2 = p2.angle, p2_speed * (p2.mass - p1.mass) / total_mass
        anglespeed1 = angle + math.pi, 2 * p1_speed * p1.mass / total_mass
        (p2.angle, p2.speed) = add_vectors(angle2speed2, anglespeed1)

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap
        return True


def contamination(p1, p2):
    """ Change the state of the particle after collision
    Args:
        p1(obj): first particle
        p2(obj): second particle
    """
    if p1.state == 1 or p2.state == 1:
        p1.colour = p2.colour = (187, 100, 29)
        p2.state = p1.state = 1


def heal_from_time(dt, particle):
    """
    Args:
        dt(int): time between two loops of pygame
        particle(obj): the particle to heal
    """
    if particle.state == 1:
        particle.time_from_contamination += dt
    if particle.time_from_contamination >= 4.0:
        particle.colour = (203, 138, 192)
        particle.state = 2


class Wall:
    def __init__(self):
        self.colour = (0, 0, 0)
        self.x = 200
        self.y = 0
        self.width = 35
        self.height = 320
        self.thickness = 4


class Particle:
    """ Main object, circular
    Args:
        xy(tuple): tuple with x and y coordinate
        size(int): size of the particle
        state(int): can be 0 (healthy), 1(sick) or 2(recovered)
        mass(int): the mass of the particle
     """

    def __init__(self, xy, size, state, mass=1, ):
        self.x, self.y = xy
        self.size = size
        self.colour = (170, 198, 202)
        self.sick_colour = (187, 100, 29)
        self.heal_colour = (203, 138, 192)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1  # 1
        self.state = state
        self.movement = True
        self.time_from_contamination = 0

    def move(self):
        """ Update position based on speed, angle"""
        if self.movement:
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed
            self.speed *= self.drag
            # Speed limiter for low number of particules
            # if self.speed > 0.1:
            #     self.speed = 0.1


class Simulation:
    """ Defines the boundary of a simulation and its properties
    Args:
        screen_dimensions(tuple): give width and height of the pygame screen
    """

    def __init__(self, screen_dimensions):
        self.width, self.height = screen_dimensions
        self.particles = []
        self.colour = (255, 255, 255)
        self.mass_of_air = 0.0  # 0.2
        self.elasticity = 1  # 0.75
        self.counter = {"healthy": 0, "sick": 0, "recovered": 0, }
        self.wall = None
        self.particle_counter = []
        self.healthy = []
        self.sick = []
        self.recovered = []

    def add_wall(self, **kwargs):
        """Add a wall to separate particles
        Args:
            'add'(bool): add or not the wall
        """
        if kwargs.get("add", False):
            self.wall = Wall()

    def add_particle(self, n=1, **kwargs):
        """ Add a number of particle in respect of arguments
         Args:
             n(int): specify then umber of particle to create
             speed(in): the initial speed particles will start with
             freezed(int): specify the percentage of particle to be immobile
             killer(int): the number of particle to be sick at the start
        """
        for i in range(n):
            size = 5
            mass = 100
            x = random.uniform(size, self.width - size)
            y = random.uniform(size, self.height - size)
            healthy = range(kwargs.get('killer', 0), n)
            if i in healthy:
                state = 0
            else:
                state = 1

            particle = Particle((x, y), size, state, mass)

            freezed = kwargs.get('freezed', 0)
            if i <= (n * freezed / 100) and state != 1:
                particle.speed = 0
                particle.movement = False
            else:
                particle.speed = kwargs.get('speed', 1)
                particle.movement = True

            particle.angle = random.uniform(0, math.pi * 2)
            if state == 1:
                particle.colour = kwargs.get('colour', (187, 100, 29))
            else:
                particle.colour = kwargs.get('colour', (170, 198, 202))
            particle.drag = (particle.mass / (
                    particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)

    def update(self, dt):
        """  Moves particle, test for collisions, give sickness, heal and
        count
        """
        for i, particle in enumerate(self.particles):
            particle.move()
            self.wall_bounce(particle)
            for particle2 in self.particles[i + 1:]:
                if collide(particle, particle2):
                    contamination(particle, particle2)
            heal_from_time(dt, particle)
            self.particle_counter.append(particle.state)
        self.healthy.append(self.particle_counter.count(0))
        self.sick.append(self.particle_counter.count(1))
        self.recovered.append(self.particle_counter.count(2))
        self.particle_counter = []

    def wall_bounce(self, particle):
        """ Test if a particle bounce on boundaries.
        Args:
            particle(obj): the particle to be tested"""

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
