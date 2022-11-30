import wireframe as wf
import pygame
import numpy as np
from const import KEY_TO_FUNCTION

class Geometry3D:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.wireframes = []
        self.nodeColour = (255, 255, 255)
        self.edgeColour = (200, 200, 200)
        self.nodeRadius = 4

    def addWireframe(self, wireframe):
        """ Add a named wireframe object. """

        self.wireframes.append(wireframe)

    def getDisplaySQFaces(self, index=None):
        faces = []

        if index == None:
            wf = self.wireframes
        else:
            wf = [self.wireframes[index]]

        for wireframe in wf:
            for i in range(wireframe.nodes.shape[0]):
                    if (i+1) % 4 == 0 and i < len(wireframe.nodes):
                        faces.append([wireframe.nodes[n1][:2] for n1, n2 in wireframe.edges[i-3:(i+1)]])
        
        return faces

    def getDisplayEdges(self, index=None):
        edges = []

        if index == None:
            wf = self.wireframes
        else:
            wf = [self.wireframes[index]]

        for wireframe in wf:
            for n1, n2 in wireframe.edges:
                edges.append((wireframe.nodes[n1][:2], wireframe.nodes[n2][:2]))
        
        return edges

    def getDisplayNodes(self, index=None):
        nodes = []

        if index == None:
            wf = self.wireframes
        else:
            wf = [self.wireframes[index]]

        for wireframe in wf:
                for node in wireframe.nodes:
                    nodes.append((int(node[0]), int(node[1])))
        
        return nodes

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes:
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the center of the screen. """

        center_x = self.width/2
        center_y = self.height/2

        for wireframe in self.wireframes:
            wireframe.scale(center_x, center_y, scale)

    def rotateAll(self, axis, theta, center=None):
        """ Rotate all wireframe about their center, along a given axis by a given angle. """

        for wireframe in self.wireframes:
            if center == None:
                center = wf.Wireframe.findCenter(wireframe.nodes)

            wireframe.rotate(axis, center, theta)

if __name__ == '__main__':
    width, height = 400, 300

    screen = pygame.display.set_mode((width, height))

    g3d = Geometry3D(width, height)

    cube = wf.Wireframe()
    cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    g3d.addWireframe('cube', cube)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_FUNCTION:
                    KEY_TO_FUNCTION[event.key](g3d)
        
        screen.fill((0, 20, 50))
        g3d.draw(screen)  
        pygame.display.flip()