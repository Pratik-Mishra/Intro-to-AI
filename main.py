import random
import math

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
def astar(maze, heuristic):
    path = []
    val = 1
    delta = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    init = [0, 0]
    goal = [len(maze)-1, len(maze[0])-1]
    visited = [[0 for j in range(len(maze[0]))] for i in range(len(maze))]
    visited[init[0]][init[1]] = 1
    expand = [[-1 for i in range(len(maze[0]))] for i in range(len(maze))]
    expand[init[0]][init[1]] = 0
    x = init[0]
    y = init[1]
    g = 0
    f = g + heuristic[x][y]
    minList = [f, g, x, y]
    while minList[2:] != goal:
        for i in range(len(delta)):
            x2 = x + delta[i][0]
            y2 = y + delta[i][1]
            if 0 <= x2 < len(maze) and 0 <= y2 < len(maze[0]):
                if visited[x2][y2] == 0 and maze[x2][y2] == 0:
                    g2 = g + 1
                    f2 = g2 + heuristic[x2][y2]
                    path.append([f2, g2, x2, y2])
                    visited[x2][y2] = 1

        if not path:
            return 'fail', expand

        del minList[:]
        minList = min(path)
        print (minList[2:])
        path.remove(minList)
        x = minList[2]
        y = minList[3]
        g = minList[1]
        expand[x][y] = val
        val += 1
        
        #print (expand)

    return minList, expand
def EuclidHeuristic(dim, maze):
    heuristic = [[0] * dim for i in range(dim)]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            heuristic[i][j] = math.sqrt((dim-1-i)**2+(dim-1-j)**2)
    for row in heuristic:
        print(' '.join([str(elem) for elem in row]))
    return heuristic

def getMin(queue):
    min = [0, 0, 999]
    for c in queue:
        if c[2] < min[2]:
            min = c
    return min

def bfs(dim, maze, heuristic):
    mazepath = maze
    mazepath[0][0] = 'P'
    start = [0, 0, heuristic[0][0]]
    path = []
    queue = []
    queue.append(start)
    visited = []
    visited.append(start)
    while queue:
        current = getMin(queue)
        queue.remove(current)
        path.append(current)
        mazepath[current[1]][current[0]] = 'P'
        print(path)
        if current[0] == 9 and current[1] == 9:
            return
        for d in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
            neighbor = [current[0]+d[0], current[1]+d[1]]
            if 0 <= neighbor[0] <= dim-1 and 0 <= neighbor[1] <= dim-1:
                neighbor.append(heuristic[neighbor[1]][neighbor[0]])
                if neighbor not in visited and maze[neighbor[1]][neighbor[0]] == 0:
                    queue.append(neighbor)
                    visited.append(neighbor)
                    mazepath[neighbor[1]][neighbor[0]] = 'V'
                    print(neighbor)
                    for row in mazepath:
                        print(' '.join([str(elem) for elem in row])) 

maze = grid(10, 0.2)
heuristic = EuclidHeuristic(10, maze)
astar(maze, heuristic)
