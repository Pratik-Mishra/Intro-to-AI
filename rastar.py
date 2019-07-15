import random
import math

class Node:
    
    def __init__(self, value, point, parent, g, h, s):
        self.value = value
        self.point = point
        self.parent = parent
        self.g = g
        self.h = h
        self.s = s
        
    def cost(self,other):
        return 0 if self.value == 1 else 1
    
def block(p):
    return 1 if random.random() < p else 0

def grid(dim, p):
    maze = [[0] * dim for i in range(dim)]
    for i in range(dim):
        for j in range(dim):
            if i is 0 and j is 0:
                maze[i][j] = 0
            elif i is dim-1 and j is dim-1:
                maze[i][j] = 0
            else:
                maze[i][j] = block(p)
##    for row in maze:
##        print(' '.join([str(elem) for elem in row]))
    return maze

def computePath(maze, openset, closedset, goal, counter):
    while goal.g > min(openset, key = lambda f:f.g + f.h).g + min(openset, key = lambda f:f.g + f.h).h:
        curr = min(openset, key = lambda f:f.g + f.h)
        openset.remove(curr)
        closedset.append(curr)
        for d in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
            neighbor = [curr.point[0]+d[0], curr.point[1]+d[1]]
            if 0 <= neighbor[0] <= len(maze)-1 and 0 <= neighbor[1] <= len(maze)-1:
                if maze[neighbor[0]][neighbor[1]] in closedset:
                    continue
                if maze[neighbor[0]][neighbor[1]].s < counter:
                    maze[neighbor[0]][neighbor[1]].g = math.inf
                    maze[neighbor[0]][neighbor[1]].s = counter
                if maze[neighbor[0]][neighbor[1]].g > curr.g+1:
                    maze[neighbor[0]][neighbor[1]].g = curr.g+1
                    maze[neighbor[0]][neighbor[1]].parent = curr
                    if maze[neighbor[0]][neighbor[1]] in openset:
                        openset.remove(maze[neighbor[0]][neighbor[1]])
                    openset.append(maze[neighbor[0]][neighbor[1]])
    return openset, closedset

def aStar(start, goal, maze, heuristic):
    counter = 0
    curr = start
    while curr.point != goal.point:
        counter += 1
        curr.g = 0
        curr.s = counter
        goal.g = math.inf
        openset = []
        closedset = []
        openset.append(curr)
        ret = computePath(maze, openset, closedset, goal, counter)
        openset = ret[0]
        closedset = ret[1]
        if not openset:
            print('Unsolvable')
        path = []
        while curr.parent:
            path.append(curr)
            curr = curr.parent
        path.append(curr)
        path = path[::-1]
        for c in path:
            print(c.point)
        break
        
    

def ManhattanHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])): 
            heuristic[i][j] = abs(dim-1-i)+abs(dim-1-j)
##    for row in heuristic:
##        print(' '.join([str(elem) for elem in row]))
    return heuristic

def part3():
    table = []
    dim = 10
    p = 0.25
    for i in range(1):
        row = []
        for j in range(1):
            maze = grid(dim, p)
            heuristic = ManhattanHeuristic(dim, maze)
            for x in range(len(maze)):
                for y in range(len(maze[x])):
                    maze[x][y] = Node(maze[x][y],[x,y], None, math.inf, heuristic[x][y], 0)
            path = aStar(maze[0][0], maze[dim-1][dim-1], maze, heuristic)
    ##for row in table:
    ##    print(' '.join([str(elem) for elem in row]))
    return path

part3()
