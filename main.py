import pygame
import numpy as np
import noise

from const import *
from geometry3d import Geometry3D
import wireframe as wf
from gnoise import GNoise

def color_blend(c1, c2, pct1):#pct1: % of c1 into the new color(i.e. pct1=0.3, that means 30% of c1 and 70% of c2 will be in the new color)
    pct2 = 1-pct1
    return [int(c1[i]*pct1+c2[i]*pct2) for i in range(len(c1))]

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

            cell_edges = edges_from_nodes(cell_nodes, len(row_nodes))
            for i in range(len(cell_nodes)):
                row_nodes.append(cell_nodes[i])
                row_edges.append(cell_edges[i])

        row_wf.addNodes(np.array(row_nodes))
        row_wf.addEdges(row_edges)

        g3d.addWireframe(row_wf)

    return g3d

def get_terrain_colors(terrain_data):
    terrain_colors = []

    for row in terrain_data:
        for corners in row:
            n = sum(corners)/len(corners)

            if n < 0:
                color = (0, min(255, max(0, 150 - abs(n) * 25)), min(255, max(0, 255 - abs(n) * 25)))
            else:
                color = (min(255, 30 - n * 10 + n * 30), min(255, 50 + n * 40 + n * 30), min(255, 50 + n * 10))
            terrain_colors.append(color)
    
    return terrain_colors

#Cube Demo Code
'''
cube = wf.Wireframe()
cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
cube.addNodes(np.array(cube_nodes))
cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

g3d.addWireframe(cube)

cube = wf.Wireframe()
cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (300,500)]
cube.addNodes(np.array(cube_nodes))
cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

g3d.addWireframe(cube)
'''

def redrawGameWindow(screen, terrain_map, terrain_colors, offset):
    screen.fill((0, 0, 0))

    terrain_faces = terrain_map.getDisplaySQFaces(offset)

    for i, face in enumerate(terrain_faces):
        color = terrain_colors[i]

        avg_y = find_center([f[Y] for f in face])
        if avg_y < GRID_SIZE*2:
            color = FOG_COLOR
        elif GRID_SIZE*2 < avg_y < HEIGHT/3:
            color = color_blend(color, FOG_COLOR, min(1, (avg_y-GRID_SIZE*2) / (HEIGHT/3)))

        pygame.draw.polygon(screen, color, face)

    # terrain_nodes = terrain_map.getDisplayNodes()
    # for node in terrain_nodes:
    #     pygame.draw.circle(screen, terrain_map.nodeColour, node, 4)

    # terrain_edges = terrain_map.getDisplayEdges()
    # for edge in terrain_edges:
    #     pygame.draw.aaline(screen, terrain_map.edgeColour, edge[0], edge[1])

    pygame.display.update()

def new_map(gnoise, rows, columns, size, offset=[0, 0]):
    noise_data = gnoise.generate_noise(rows, columns, size, TRANSFORMATION, offset)

    # noise_data = np.zeros((rows*size, columns*size))
    # for row in range(noise_data.shape[0]):
    #     for col in range(noise_data.shape[1]):
    #         noise_data[row][col] = noise.pnoise2((col*size+offset[0])/noise_data.shape[1], (row*size+offset[1])/noise_data.shape[0], octaves=2)
    #         noise_data[row][col] = TRANSFORMATION(noise_data[row][col])

    terrain_data = get_terrian_data(noise_data)
    terrain_map = generate_map(terrain_data, GRID_SIZE)

    # Set Up Transformations
    terrain_map.rotateAll(X, 200)
    terrain_map.translateAll(X, -(terrain_map.wireframes[0].nodes[-1][X]-WIDTH)/2)
    terrain_map.translateAll(Y, HEIGHT-terrain_map.wireframes[0].nodes[-1][Y])

    terrain_colors = get_terrain_colors(terrain_data)

    return terrain_map, terrain_colors


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Noise Scroller")
    clock = pygame.time.Clock()

    rows, columns, size = 20, 4, 8

    gnoise = GNoise((WIDTH, HEIGHT))

    terrain_map, terrain_colors = new_map(gnoise, rows, columns, size)

    offset = [0, 0]

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_FUNCTION:
                    KEY_TO_FUNCTION[event.key](terrain_map)

        # if offset[1] > int(terrain_map.wireframes[0].nodes[0][Y]):
        #     terrain_map, terrain_colors = new_map(gnoise, rows, columns, size, [0, rows])
        offset[1] += SCROLL_SPEED

        redrawGameWindow(screen, terrain_map, terrain_colors, offset)
    pygame.quit()

if __name__ == "__main__":
    main()