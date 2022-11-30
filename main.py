import pygame
import numpy as np
import copy
import noise

from const import *
from geometry3d import Geometry3D
import wireframe as wf
from gnoise import GNoise


def get_terrian_data(noise_data):
    terrain_data = []
    for row in range(len(noise_data)-1):
        terrain_data.append([])
        for col in range(len(noise_data[row])-1):
            terrain_data[row].append([])
            terrain_data[row][col].append(noise_data[row][col])
            terrain_data[row][col] += list(noise_data[row+1][col:col+2])
            terrain_data[row][col].append(noise_data[row][col+1])
    
    return terrain_data

def edges_from_nodes(nodes, node_offset):
    edges = []
    for i in range(len(nodes)):
        if i+node_offset == node_offset+3:
            edges.append((i+node_offset, node_offset))#otherwise, the last node to the first node
        else:
            edges.append((i+node_offset, i+node_offset+1))#following the nodes to connect the shape
    
    return edges

def generate_map(terrain_data, size):
    g3d = Geometry3D(WIDTH, HEIGHT)
    
    water_wf = wf.Wireframe()
    for row in range(len(terrain_data)):
        row_wf = wf.Wireframe()

        row_nodes = []
        row_edges = []
        
        for col in range(len(terrain_data[row])):
            cell = terrain_data[row][col]

            lt_x = col*size
            lb_x = col*size
            t_z = row*size

            rt_x = lt_x + size
            rb_x = lb_x + size
            b_z = t_z + size

            cell_nodes = [[lt_x, cell[0]*size, t_z], [lb_x, cell[1]*size, b_z], [rb_x, cell[2]*size, b_z], [rt_x, cell[3]*size, t_z]]

            # cell_edges = edges_from_nodes(cell_nodes, len(row_nodes))
            # for i in range(len(cell_nodes)):
            #     row_nodes.append(cell_nodes[i])
            #     row_edges.append(cell_edges[i])

            row_offset = len(row_nodes)
            for i in range(len(cell_nodes)):
                
                if i+row_offset == row_offset+3:
                    row_edges.append((i+row_offset, row_offset))#otherwise, the last node to the first node
                else:
                    row_edges.append((i+row_offset, i+row_offset+1))#following the nodes to connect the shape

                row_nodes.append(cell_nodes[i])

            # y_mean = sum(cell)/len(cell)
            # if y_mean < 0:
            #     water_wf.addNodes([[node[0], 0, node[2]] for node in cell_nodes])
            #     water_wf.addEdges(cell_edges)

        row_wf.addNodes(np.array(row_nodes))
        row_wf.addEdges(row_edges)

        g3d.addWireframe(row_wf)
        # g3d.addWireframe(water_wf)

    return g3d

# cube = wf.Wireframe()
# cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
# cube.addNodes(np.array(cube_nodes))
# cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

# g3d.addWireframe(cube)

# cube = wf.Wireframe()
# cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (300,500)]
# cube.addNodes(np.array(cube_nodes))
# cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

# g3d.addWireframe(cube)

rows, columns = 24, 24

gnoise = GNoise((rows, columns))
noise_data = gnoise.generate_noise(4, lambda x: x*3 + 0.5)

# noise_data = np.zeros((rows*4, columns*4))
# for row in range(noise_data.shape[0]):
#     for col in range(noise_data.shape[1]):
#         noise_data[row][col] = noise.pnoise2(col*4/noise_data.shape[1], row*4/noise_data.shape[0], octaves=2) * 3

terrain_data = get_terrian_data(noise_data)
terrain_map = generate_map(terrain_data, GRID_SIZE)

# print([ for node in terrain_map.wireframes[0]])

terrain_faces = terrain_map.getDisplaySQFaces()
terrain_colors = []# [color: (0, 0, 0), water: bool]

for row in terrain_data:
    for corners in row:
        n = sum(corners)/len(corners)

        color = [0, 0, 0]
        if n < 0:
            color = (0, min(255, max(0, 150 - abs(n) * 25)), min(255, max(0, 255 - abs(n) * 25)))
        else:
            color = (min(255, 30 - n * 10 + n * 30), min(255, 50 + n * 40 + n * 30), min(255, 50 + n * 10))
        terrain_colors.append(color)

offset = [0, 0]
def redrawGameWindow(screen):
    screen.fill((0, 0, 0))

    terrain_faces = terrain_map.getDisplaySQFaces()

    for i, face in enumerate(terrain_faces):

        pygame.draw.polygon(screen, terrain_colors[i], face)
        if sum([f[1]-offset[1] for f in face])/len(face) < 0:
            pygame.draw.polygon(screen, terrain_colors[i], [[f[0], offset[1]] for f in face])

    # terrain_nodes = terrain_map.getDisplayNodes()
    # for node in terrain_nodes:
    #     pygame.draw.circle(screen, terrain_map.nodeColour, node, 4)

    # terrain_edges = terrain_map.getDisplayEdges()
    # for edge in terrain_edges:
    #     pygame.draw.aaline(screen, terrain_map.edgeColour, edge[0], edge[1])

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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset[0] += -SPEED
                elif event.key == pygame.K_RIGHT:
                    offset[0] += SPEED
                elif event.key == pygame.K_UP:
                    offset[1] += -SPEED
                elif event.key == pygame.K_DOWN:
                    offset[1] += SPEED

                if event.key in KEY_TO_FUNCTION:
                    KEY_TO_FUNCTION[event.key](terrain_map)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     lambda x: x.translateAll(X, -SPEED)),
    # elif keys[pygame.K_RIGHT:  (lambda x: x.translateAll(X,  SPEED)),
    # elif keys[pygame.K_UP]:lambda x: x.translateAll(Y, -SPEED)),
    # elif keys[pygame.K_DOWN]:lambda x: x.translateAll(Y,  SPEED)),
    # elif keys[pygame.K_COMMA]:lambda x: x.translateAll(Z, -SPEED)),
    # elif keys[pygame.K_PERIOD]:lambda x: x.translateAll(Z, SPEED)),
    # elif keys[pygame.K_q]:lambda x: x.rotateAll(X,  ROTATE_INCREMENT, ROTATE_AXIS)),
    # elif keys[pygame.K_w]:lambda x: x.rotateAll(X, -ROTATE_INCREMENT, ROTATE_AXIS)),
    # elif keys[pygame.K_a]:lambda x: x.rotateAll(Y,  ROTATE_INCREMENT, ROTATE_AXIS)),
    # elif keys[pygame.K_s]:lambda x: x.rotateAll(Y, -ROTATE_INCREMENT, ROTATE_AXIS)),

        redrawGameWindow(screen)
    pygame.quit()

if __name__ == "__main__":
    main()