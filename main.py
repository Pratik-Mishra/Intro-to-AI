import random
import math

def block(p):
    return 'B' if random.random() < p else 'U'

def grid(dim, p):
    maze = [[0] * dim for i in range(dim)]
    for i in range(dim):
        for j in range(dim):
            if i is 0 and j is 0:
                maze[i][j] = 'S'
            elif i is dim-1 and j is dim-1:
                maze[i][j] = 'G'
            else:
                maze[i][j] = block(p)
    for row in maze:
        print(' '.join([str(elem) for elem in row]))
    return maze

def CompletePath(maze):
    current = Node([0,0], math.inf, euclidean, None)
    OPEN = []
    CLOSED = []
    OPEN.append(start)
    while current.h is not 0:
        
    
class Node:
    def __init__(self, coordinate, g, h, prev):
        self.coordinate = coordinate
        self.g = g
        self.h = h
        self.prev = prev
        
def Main:        
        
    
    
maze = grid(10, 0.2)
            
    

    
