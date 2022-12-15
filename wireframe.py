import numpy as np
import math
from const import X, Y, Z, DIMENSIONS

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []
        self.node_colors = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def outputNodes(self):
        for i in range(self.nodes.shape[1]):
            x, y, z, _ = self.nodes[i]
            print("Node %d: (%.3f, %.3f, %.3f)" % (i, x, y, z))
            
    def outputEdges(self):
        for i, (start, stop) in enumerate(self.edges):
            node1 = self.nodes[:, start]
            node2 = self.nodes[:, stop]
            print("Edge %d: (%.3f, %.3f, %.3f)" % (i, node1[0], node1[1], node1[2]), "to (%.3f, %.3f, %.3f)" % (node2[0], node2[1], node2[2]))

    def translate(self, axis, d):
        """ Add constant 'd' to the coordinate 'axis' of each node of a wireframe """

        for node in self.nodes:
            node[axis] += d

    def scale(self, center_x, center_y, scale):
        """ Scale the wireframe from the center of the screen """

        for node in self.nodes:
            node[X] = center_x + scale * (node[0] - center_x)
            node[Y] = center_y + scale * (node[1] - center_y)
            node[Z] *= scale

    def rotate(self, axis, center, degrees):
        cx,cy,cz = center

        if axis == X:
            for node in self.nodes:
                y      = node[Y] - cy
                z      = node[Z] - cz
                d      = math.hypot(y, z)
                theta  = math.atan2(y, z) + math.radians(degrees)

                node[Y] = cy + d * math.sin(theta)
                node[Z] = cz + d * math.cos(theta)

        elif axis == Y:
            for node in self.nodes:
                x      = node[X] - cx
                z      = node[Z] - cz
                d      = math.hypot(x, z)
                theta  = math.atan2(x, z) + math.radians(degrees)
                node[X] = cx + d * math.sin(theta)
                node[Z] = cz + d * math.cos(theta)

        elif axis == Z:
            for node in self.nodes:
                x      = node[X] - cx
                y      = node[Y] - cy
                d      = math.hypot(y, x)
                theta  = math.atan2(y, x) + math.radians(degrees)
                node[X] = cx + d * math.cos(theta)
                node[Y] = cy + d * math.sin(theta)

if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
    cube.addNodes(np.array(cube_nodes))
    
    cube.addEdges([(n,n+4) for n in range(0,4)])
    cube.addEdges([(n,n+1) for n in range(0,8,2)])
    cube.addEdges([(n,n+2) for n in (0,1,4,5)])
    
    cube.outputNodes()
    cube.outputEdges()