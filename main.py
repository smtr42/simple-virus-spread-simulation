import pygame

import particle

pygame.display.set_caption('Tutorial 10')
screen_dimensions = (800, 600)
screen = pygame.display.set_mode(screen_dimensions)
sim = particle.Simulation(screen_dimensions)

# sim.add_particle(10)
sim.add_particle(n=150, speed=6, freezed=90, killer=3)
timer = pygame.time.Clock()
elapsed_time = 0

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

    pygame.display.flip()
