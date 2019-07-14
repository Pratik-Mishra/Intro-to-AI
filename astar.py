import time
import random
import math

class Node:
    
    def __init__(self,value,point, parent, g, h):
        self.value = value
        self.point = point
        self.parent = parent
        self.g = g
        self.h = h
        
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

def children(curr, maze):
    x, y = curr.point
    links = []
    for d in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
            neighbor = [curr.point[0]+d[0], curr.point[1]+d[1]]
            if 0 <= neighbor[0] <= len(maze)-1 and 0 <= neighbor[1] <= len(maze)-1:
                if maze[neighbor[0]][neighbor[1]].value == 0:
                    links.append(maze[neighbor[0]][neighbor[1]])
    return links

def aStar(start, goal, maze, heuristic):
    openset = []
    closedset = []
    curr = start
    openset.append(curr)
    path = []
    while openset:
        curr = min(openset, key = lambda f:f.g + f.h)
        if curr.point == goal.point:
            while curr.parent:
                path.append(curr)
                curr = curr.parent
            path.append(curr)
            return path[::-1]
        openset.remove(curr)
        closedset.append(curr)
        for node in children(curr, maze):
            if node in closedset:
                continue
            elif node in openset:
                new_g = curr.g + curr.cost(node)
                if node.g > new_g:
                    node.g = new_g
                    node.parent = curr
            else:
                node.g = curr.g + curr.cost(node)
                node.h = heuristic[node.point[0]][node.point[1]]
                node.parent = curr
                openset.append(node)
    print('Unsolvable')
    return path
            
def EuclidHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            heuristic[i][j] = math.sqrt((dim-1-i)**2+(dim-1-j)**2)
##    for row in heuristic:
##        print(' '.join([str(elem) for elem in row]))
    return heuristic

def ManhattanHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])): 
            heuristic[i][j] = abs(dim-1-i)+abs(dim-1-j)
##    for row in heuristic:
##        print(' '.join([str(elem) for elem in row]))
    return heuristic

def ChebyshevHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            heuristic[i][j] = max(abs(dim-1-i),abs(dim-1-j))
##    for row in heuristic:
##        print(' '.join([str(elem) for elem in row]))
    return heuristic

def part1():
    table = []
    dim = 101
    p = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    for i in p:
        row = []
        for j in range(50):
            maze = grid(dim, i)
            heuristic = EuclidHeuristic(dim, maze)
            for x in range(len(maze)):
                for y in range(len(maze[x])):
                    maze[x][y] = Node(maze[x][y],[x,y], None, 0, heuristic[x][y])
            path = aStar(maze[0][0], maze[dim-1][dim-1], maze, heuristic)
            if path:
                row.append(1)
            else:
                row.append(0)
        table.append(row)
    for row in table:
        print(' '.join([str(elem) for elem in row]))

def part2():
    table = []
    dim = 101
    p = 0.25
    for i in range(3):
        row = []
        for j in range(50):
            maze = grid(dim, p)
            if i is 0:
                heuristic = EuclidHeuristic(dim, maze)
            elif i is 1:
                heuristic = ManhattanHeuristic(dim, maze)
            elif i is 2:
                heuristic = ChebyshevHeuristic(dim, maze)
            for x in range(len(maze)):
                for y in range(len(maze[x])):
                    maze[x][y] = Node(maze[x][y],[x,y], None, 0, heuristic[x][y])
            start_time = time.time()
            path = aStar(maze[0][0], maze[dim-1][dim-1], maze, heuristic)
            runtime = round(time.time() - start_time, 2)
            if path:
                row.append(runtime)
        table.append(row)
    for row in table:
        print(sum(row)/len(row))
part1()
part2()



