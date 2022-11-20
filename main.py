import pygame
from const import *

def redrawGameWindow(screen):
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 100, 100))

    pygame.display.update()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot Set")
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        redrawGameWindow(screen)
    pygame.quit()

if __name__ == "__main__":
    main()