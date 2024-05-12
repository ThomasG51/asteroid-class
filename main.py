import pygame
import sys

# init
pygame.init()

# settings
window_width = 1280
window_height = 720
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Asteroid")

# game loop
while True:
    # delta time
    dt = clock.tick(120) / 1000

    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # update

    # draw surface

    # show the 'display surface'
    pygame.display.update()