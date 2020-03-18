import pygame
import particle

pygame.display.set_caption('Tutorial 10')
wh = (800, 600)
screen = pygame.display.set_mode(wh)
env = particle.Environment(wh)

env.addParticles(15)
env.addParticles(x=200, y=250, size=10, speed=1, angle=0)
timer = pygame.time.Clock()

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         selected_particle = env.findParticle(pygame.mouse.get_pos())
    #     elif event.type == pygame.MOUSEBUTTONUP:
    #         selected_particle = None
    #
    # if selected_particle:
    #     selected_particle.mouseMove(pygame.mouse.get_pos())

    dt = timer.tick() / 1000

    env.update()
    screen.fill(env.colour)

    for p in env.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)

    pygame.display.flip()