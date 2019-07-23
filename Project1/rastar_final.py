import random
import math
import time

## The Node class has 7 attributes. Value (1/0) represents a blocked or unblocked cell respectively. Point refers to the Node's coordinates.
## Parent denotes the parent cell of the Node. G is the cell's g value, h is the cell's h value, and s is the cell's search value. C is the cost
## to get to that cell.
class Node:
    
    def __init__(self, value, point, parent, g, h, s, c):
        self.value = value
        self.point = point
        self.parent = parent
        self.g = g
        self.h = h
        self.s = s
        self.c = c
        
    def cost(self,other):
        return 0 if self.value == 1 else 1
    
def block(p):
    return 1 if random.random() < p else 0

## Based on parameters dim (dimension) and p (blocked cell probability), this function will create a dim x dim grid and return that grid.
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
    ##for row in maze:
    ##    print(' '.join([str(elem) for elem in row]))
    return maze

## Compute path will compute a path from the given start node in the openset to the goal node. The tie_desc variable will sort the openset in order
## of descending g values when True, so that when min() is called and there are multiple smallest f values, it will pick the first, which will also
## the largest g value. The rest of the code follows the given project pseudocode.
def computePath(maze, openset, closedset, goal, counter, tie_desc):
    if tie_desc is True:
        openset.sort(key = lambda o:o.g, reverse=True)
    else:
        openset.sort(key = lambda o:o.g)
    while openset and goal.g > min(openset, key = lambda f:f.g + f.h).g + min(openset, key = lambda f:f.g + f.h).h:
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
                    if maze[neighbor[0]][neighbor[1]].g > curr.g+maze[neighbor[0]][neighbor[1]].c and maze[neighbor[0]][neighbor[1]].c < 2:
                        maze[neighbor[0]][neighbor[1]].g = curr.g+maze[neighbor[0]][neighbor[1]].c
                        maze[neighbor[0]][neighbor[1]].parent = curr
                        if maze[neighbor[0]][neighbor[1]] in openset:
                            openset.remove(maze[neighbor[0]][neighbor[1]])
                        openset.append(maze[neighbor[0]][neighbor[1]])
    return openset

## This portion of code follows the Main() section of the given project pseudocode. When the openset becomes empty, then the problem is unsolvable. This
## function returns 0 if unsolvable, and 1 otherwise.
def aStar(start, goal, maze, heuristic, tie_desc):
    counter = 0
    while start.point != goal.point:
        counter += 1
        start.g = 0
        start.s = counter
        goal.g = math.inf
        openset = []
        closedset = []
        openset.append(start)
        openset = computePath(maze, openset, closedset, goal, counter, tie_desc)
        if not openset:
            print('Unsolvable')
            return 0
        path = []
        curr = goal
        while curr.point != start.point:
            path.append(curr)
            curr = curr.parent
        path = path[::-1]
        prev = curr
        for p in path:
            if maze[p.point[0]][p.point[1]].value == 0:
                prev = p
                continue
            else:
                maze[p.point[0]][p.point[1]].c += 1
                break
        start = prev
    return 1

## This is the heuristic function which will create a secondary grid of only heuristic values, matching the main maze grid.
def ManhattanHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])): 
            heuristic[i][j] = abs(dim-1-i)+abs(dim-1-j)
##    for row in heuristic:
##        print(' '.join([str(elem) for elem in row]))
    return heuristic

## This function is used to test part 3a.
def part3():
    table = []
    dim = 101
    p = 0.25
    tie_desc = False
    for i in range(1):
        row = []
        for j in range(10):
            maze = grid(dim, p)
            heuristic = ManhattanHeuristic(dim, maze)
            for x in range(len(maze)):
                for y in range(len(maze[x])):
                    maze[x][y] = Node(maze[x][y],[x,y], None, math.inf, heuristic[x][y], 0, 1)
            start = time.time()
            ret = aStar(maze[0][0], maze[dim-1][dim-1], maze, heuristic, tie_desc)
            runtime = time.time()-start
            if ret == 1:
                row.append(runtime)
    print(sum(row)/len(row))
    return path

## This function is used to test part 4a.
def part4():
    table = []
    dim = 101
    p = 0.25
    tie_desc = True
    for i in range(1):
        forwards = []
        backwards = []
        for j in range(10):
            maze = grid(dim, p)
            maze2 = []
            for x in maze:
                y = x[::-1]
                maze2.append(y)
            maze2 = maze2[::-1]
            ##for row in maze2:
            ##    print(' '.join([str(elem) for elem in row]))

            heuristic = ManhattanHeuristic(dim, maze)
            for x in range(len(maze)):
                for y in range(len(maze[x])):
                    maze[x][y] = Node(maze[x][y],[x,y], None, math.inf, heuristic[x][y], 0, 1)
            start = time.time()
            f = aStar(maze[0][0], maze[dim-1][dim-1], maze, heuristic, tie_desc)
            runtime = time.time()-start
            if f == 1:
                forwards.append(runtime)
            print('ok')
            
            for x in range(len(maze2)):
                for y in range(len(maze2[x])):
                    maze2[x][y] = Node(maze2[x][y],[x,y], None, math.inf, heuristic[x][y], 0, 1)
            start = time.time()
            b = aStar(maze2[0][0], maze2[dim-1][dim-1], maze2, heuristic, tie_desc)
            runtime = time.time()-start
            if b == 1:
                backwards.append(runtime)
    print(sum(forwards)/len(forwards))
    print(sum(backwards)/len(backwards))

##part3()
part4()
