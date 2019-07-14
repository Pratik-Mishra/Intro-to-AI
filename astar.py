import random
import math

class Node:
    
    def __init__(self,value,point):
        self.value = value
        self.point = point
        self.parent = None
        self.g = 0
        self.h = 0
        
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
    for row in maze:
        print(' '.join([str(elem) for elem in row]))
    return maze

def children(curr, maze):
    x, y = curr.point
    links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]]
    return [link for link in links if link.value != '%']

def aStar(start, goal, maze, heuristic):
    openset = []
    closedset = []
    curr = start
    openset.append(curr)
    while openset:
        curr = min(openset, key = lambda o:o.g + o.h)
        if curr == goal:
            path = []
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
                node.h = heuristic[node.value[0]][node.value[1]]
                node.parent = curr
                openset.append(node)
    raise ValueError('Unsolvable')
            
def EuclidHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            heuristic[i][j] = math.sqrt((dim-1-i)**2+(dim-1-j)**2)
    for row in heuristic:
        print(' '.join([str(elem) for elem in row]))
    return heuristic

maze = grid(6, 0.3)
heuristic = EuclidHeuristic(6, maze)
for x in range(len(maze)):
        for y in range(len(maze[x])):
            maze[x][y] = Node(maze[x][y],[x,y])
path = aStar([0,0], [5,5], maze, heuristic)
print (len(path) - 1)
for node in path:
    x, y = node.point
    print (x, y)
