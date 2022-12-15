import pygame
import numpy as np
import random, math

class NoiseOutOfBoundsError(Exception):
    pass
    
class GNoise:
    def __init__(self, size):#initialize a new noise object with a given then use it to calculate noise at a given coordinate.
        self.rows, self.columns = size
        self.grid = self.gradient_vectors()

    def randomize_noise(self):#redo gradient vectors for a new noise.
        self.grid = self.gradient_vectors()

    #Calculate all the corner vectors for a given size.
    def gradient_vectors(self):
        grid = np.zeros([self.rows+1, self.columns+1]+[2])#size+1 otherwise, it would be missing a vector on the right and bottom size
        
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                theta = random.randint(0, 360)
                grid[row][col] = [math.cos(theta), math.sin(theta)]#unit vector
                
        return grid

    # Linearly interpolation between a0 and a1. Weight w should be in the range [0.0, 1.0].
    def lerp(self, a0, a1, w):
        return a0 + (a1 - a0) * w

    # Cubic interpolation between a0 and a1. Weight w should be in the range [0.0, 1.0].
    def smoothstep(self, a0, a1, w):
        return (a1 - a0) * (3 - w * 2) * w * w + a0

    # Cubic interpolation between a0 and a1, with a second derivative equal to zero on boundaries. Weight w should be in the range [0.0, 1.0].
    def smootherstep(self, a0, a1, w):
        return (a1 - a0) * ((w * (w * 6 - 15) + 10) * w * w * w) + a0

    # Computes the dot product of the distance and gradient vectors.
    def dot_gradientDistance(self, gx, gy, x, y):
        #Get gradient from integer coordinates
        gradient = self.grid[gx][gy]

        # Compute the distance vector
        dx = x - gx
        dy = y - gy

        #Compute the dot-product
        return (dx*gradient[0] + dy*gradient[1])

    #Calculate gradient noise at a given point
    def noise(self, x, y):
        if -1 < x < self.columns:
            if -1 < y < self.rows:
                x0 = math.floor(x)#top corner cell coordinate
                y0 = math.floor(y)

                x1 = x0 + 1#bottom corner cell coordinate
                y1 = y0 + 1

                wx = x - x0
                wy = y - y0

                vtl = self.dot_gradientDistance(x0, y0, x, y)
                vtr = self.dot_gradientDistance(x1, y0, x, y)
                it = self.smootherstep(vtl, vtr, wx)

                vbl = self.dot_gradientDistance(x0, y1, x, y)
                vbr = self.dot_gradientDistance(x1, y1, x, y)

                ib = self.smootherstep(vbl, vbr, wx)

                value = self.smootherstep(it, ib, wy)

                return value
            else:
                raise NoiseOutOfBoundsError("'y' value out of range")
        else:
            raise NoiseOutOfBoundsError("'x' value out of range")

    def draw_grid(self, screen, offset, size):
        x_offset, y_offset = offset
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                x, y = self.grid[row][col]
                
                pygame.draw.rect(screen, (0, 0, 255), (x_offset+row*size, y_offset+col*size, size, size), 2)
                pygame.draw.aaline(screen, (255, 0, 0), (x_offset+row*size, y_offset+col*size), (x_offset+row*size + x*size, y_offset+col*size + y*size))
                pygame.draw.circle(screen, (255, 0, 0), (x_offset+row*size + x*size, y_offset+col*size + y*size), 2)

    def generate_noise(self, rows, columns, size, func=lambda x:x, offset=[0, 0]):#offset: coordinates[x, y], size: # of values between cells, func: mutation to noise
        noise_grid = np.zeros((rows*size, columns*size))

        for row in range(noise_grid.shape[0]):
            for col in range(noise_grid.shape[1]):
                noise_grid[row][col] = func(self.noise(col/size+offset[0], row/size+offset[1]))
    
        return noise_grid

def draw_noise(screen, grid, offset, size=1):
    x, y = offset

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = int((grid[row][col]*0.5+0.5)*255)
            pygame.draw.rect(screen, (color, color, color), (x+col*size, y+row*size, size, size))
    
def redrawGameWindow(screen):
    screen.fill((0, 0, 0))

    draw_noise(screen, noise_grid1, (0, 100), 2)
    draw_noise(screen, noise_grid2, (200, 100), 2)

    pygame.display.update()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Noise Scroller")
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
    import matplotlib.pyplot as plt
    import noise

    from const import *
    
    rows, columns = 20, 4
    size = 8

    gnoise = GNoise((WIDTH, HEIGHT))
    noise_grid1 = gnoise.generate_noise(rows, columns, size)

    noise_grid2 = np.zeros((rows*size, columns*size))
    for row in range(noise_grid2.shape[0]):
        for col in range(noise_grid2.shape[1]):
            noise_grid2[row][col] = noise.pnoise2(col*size/noise_grid2.shape[1], row*size/noise_grid2.shape[0], octaves=1)

    # plotting
    plt.title("Noise Plot")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")

    x = list(range(noise_grid1.shape[0]*noise_grid1.shape[1]))
    y = noise_grid1.flatten()
    plt.plot(x, y, label="noise_grid1" , color= "green")

    x = list(range(noise_grid2.shape[0]*noise_grid2.shape[1]))
    y = noise_grid2.flatten()
    plt.plot(x, y, label="noise_grid2", color= "red")
    plt.show()

    main()