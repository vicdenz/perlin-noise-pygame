import pygame


WIDTH = 600
HEIGHT = 600

GRID_SIZE = 20

FPS = 60

X = 0
Y = 1
Z = 2

DIMENSIONS = [X, Y, Z]

SPEED = 10
SCALE = 0.2
ROTATE_INCREMENT = 10

ROTATE_AXIS = None#(0, 0, 0)

HEIGHT_COLORS = {0: (24, 56, 240), }

KEY_TO_FUNCTION = {
    pygame.K_LEFT:   (lambda x: x.translateAll(X, -SPEED)),
    pygame.K_RIGHT:  (lambda x: x.translateAll(X,  SPEED)),
    pygame.K_UP:   (lambda x: x.translateAll(Y, -SPEED)),
    pygame.K_DOWN:   (lambda x: x.translateAll(Y,  SPEED)),
    pygame.K_COMMA:     (lambda x: x.translateAll(Z, -SPEED)),
    pygame.K_PERIOD:     (lambda x: x.translateAll(Z, SPEED)),
    pygame.K_EQUALS: (lambda x: x.scaleAll(1 + SCALE)),
    pygame.K_MINUS:  (lambda x: x.scaleAll(1 - SCALE)),
    pygame.K_q:      (lambda x: x.rotateAll(X,  ROTATE_INCREMENT, ROTATE_AXIS)),
    pygame.K_w:      (lambda x: x.rotateAll(X, -ROTATE_INCREMENT, ROTATE_AXIS)),
    pygame.K_a:      (lambda x: x.rotateAll(Y,  ROTATE_INCREMENT, ROTATE_AXIS)),
    pygame.K_s:      (lambda x: x.rotateAll(Y, -ROTATE_INCREMENT, ROTATE_AXIS)),
    pygame.K_z:      (lambda x: x.rotateAll(Z,  ROTATE_INCREMENT, ROTATE_AXIS)),
    pygame.K_x:      (lambda x: x.rotateAll(Z, -ROTATE_INCREMENT, ROTATE_AXIS))
}