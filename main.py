import pygame
from graph import Grapher
import particle
import os
x = 100
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.display.set_caption('Tutorial 10')
screen_dimensions = (800, 400)
screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption("Covid spread simulation")

sim = particle.Simulation(screen_dimensions)
graph = Grapher()

sim.add_particle(n=150, speed=6, freezed=93, killer=4)
sim.add_wall(add=False)

timer = pygame.time.Clock()
elapsed_time = 0
time_serie=[]

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = timer.tick() / 1000
    sim.update(dt)
    screen.fill(sim.colour)

    for p in sim.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size,
                           p.thickness)

    if isinstance(sim.wall, particle.Wall):
        pygame.draw.rect(screen, sim.wall.colour, (
        sim.wall.x, sim.wall.y, sim.wall.width, sim.wall.height),
                         sim.wall.thickness)
    pygame.display.flip()
    elapsed_time += dt
    time_serie.append(elapsed_time)

    # graph.plot_healthy(time_serie, sim.healthy)
    # graph.plot_sick(time_serie, sim.sick)
    # graph.show()