import random
import statistics

p_flat = .1
p_hilly = .3
p_forest = .7
p_maze = .9
p_compliment = [1, .9, .7, .3, .1] 
types = ["flat", "hilly", "forested", "cave"]

## Each cell in the dim x dim grid takes the form [type, target] where type can be 1, 2, 3, or 4 for
## flat, hilly, forest, and maze respectively. If target is 1, then that cell is the target, otherwise
## it is 0.
def grid(dim):
    env = [[0] * dim for i in range(dim)]
    for i in range(dim):
        for j in range(dim):
            rng = random.randint(1, 100)
            if 1 <= rng <= 20:
                env[i][j] = [1, 0]
            if 21 <= rng <= 50:
                env[i][j] = [2, 0]
            if 51 <= rng <= 80:
                env[i][j] = [3, 0]
            if 81 <= rng <= 100:
                env[i][j] = [4, 0]
    target = random.randint(0, dim*dim-1)
    env[int(target/dim)][target%dim][1] = 1
    print("target placed at (" +  str(target%dim) + ", " + str(int(target/dim)) + "), which is " + types[env[int(target/dim)][target%dim][0]-1])
##    print("grid:")
##    for row in env:
##        print(' '.join([str(elem) for elem in row]))
    return env

## Each cell in the belief grid initially takes the form [type, probability], where type for all is unknown (0)
## and the probability is 1/(# of cells)
def blf_grid(dim, move):
    blf = []
    for i in range(dim):
        row = []
        for j in range(dim):
            if move:
                row.append([0, 0])
            else:
                row.append([0, 1/(dim*dim)])
        blf.append(row)
##    for row in blf:
##        print(' '.join([str(elem) for elem in row]))
    return blf

def Manhattan(x, y, i, j):
    if (abs(x-i)+abs(y-j)) == 0:
        return .99
    return abs(x-i)+abs(y-j)

def update_blf(blf, i, j, old_blf, dim):
    blf_value = blf[i][j][1]
    scale = 1
    if blf[i][j][0] == 1:
        scale += old_blf*(1 - p_flat)/(1 - old_blf)
    if blf[i][j][0] == 2:
        scale += old_blf*(1 - p_hilly)/(1 - old_blf)
    if blf[i][j][0] == 3:
        scale += old_blf*(1 - p_forest)/(1 - old_blf)
    if blf[i][j][0] == 4:
        scale += old_blf*(1 - p_maze)/(1 - old_blf)
    for x in range(dim):
        for y in range(dim):
            if not (x == i and y == j):
                blf[x][y][1] *= scale
##    print()
##    for row in blf:
##        print(' '.join([str(elem) for elem in row]))
    return blf

## Given a belief grid and its dimensions, pick the cell with the highest probability to contain the target.
## If rule = 1 (Rule #2), then the probability is scaled with the cell's probability of a false negative (otherwise normal scaling).
## If action = 1, then the probability is also scaled by the distance (Manhattan) between the current node and the candidate
def next_cell(blf, x, y, dim, rule, action):
    max = -1
    coord = []
    factor = 1
    distance = 1
    ties = []
    for i in range(dim):
        for j in range(dim):
            if action:
                distance = Manhattan(x, y, i, j)
            if rule:
                factor = p_compliment[blf[i][j][0]]
            if blf[i][j][1]*factor/distance == max:
                ties.append([i, j])
            if blf[i][j][1]*factor/distance > max:
                max = blf[i][j][1]
                ties = [[i, j]]
    coord = ties[random.randint(0, len(ties)-1)]
##    print("Next cell is (" + str(coord[1]) + ", " + str(coord[0]) + ")")
    return coord

def search(env, blf, dim, rule, action):
    counter = 1
    i = 0
    j = 0
    found = 0
    while not found:
        blf[i][j][0] = env[i][j][0]
        old_blf = blf[i][j][1]
        rng = random.randint(1, 10)
        if blf[i][j][0] == 1:
            if rng > 1:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_flat
        if blf[i][j][0] == 2:
            if rng > 3:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_hilly
        if blf[i][j][0] == 3:
            if rng > 7:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_forest
        if blf[i][j][0] == 4:
            if rng > 9:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_maze
        blf = update_blf(blf, i, j, old_blf, dim)
        coord = next_cell(blf, i, j, dim, rule, action)
        i = coord[0]
        j = coord[1]
        counter += 1
    return [counter, j, i]

def move_target(env, dim):
##    print()
##    for row in env:
##        print(' '.join([str(elem) for elem in row]))
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    border = []
    for i in range(dim):
        for j in range(dim):
            if env[i][j][1] == 1:
                env[i][j][1] = 0
                border.append(env[i][j][0])
                break
        else:
            continue
        break
##    print("Target removed from (" + str(j) + ", " + str(i) + ")") 
    move = random.randint(0, 3)
    new = [i+directions[move][0], j+directions[move][1]]
    while not (0 <= new[0] <= dim-1) or not (0 <= new[1] <= dim-1):
        new = [i, j]
        move = random.randint(0, 3)
        new = [i+directions[move][0], j+directions[move][1]]
    env[new[0]][new[1]][1] = 1
    border.append(env[new[0]][new[1]][0])
    borders = [border, border[::-1]]
##    print("Target moved to (" + str(new[1]) + ", " + str(new[0]) + ") from (" + str(j) + ", " + str(i) + ") across a " + str(types[border[0]-1]) + "/" + str(types[border[1]-1]) + " border")
##    for row in env:
##        print(' '.join([str(elem) for elem in row]))
    return env, borders

def update_blf_mv(blf, dim, border):
##    print("Border: " + str(border))
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    total = 0
    crossings = 0
    for i in range(dim):
        for j in range(dim):
            if not (blf[i][j][0] == border[0][0] or blf[i][j][0] == border[0][1]):
                blf[i][j][1] = 0
                continue
            cross = [blf[i][j][0], 0]
            for d in directions:
                neighbor = [i+d[0], j+d[1]]
                if 0 <= neighbor[0] <= dim-1 and 0 <= neighbor[1] <= dim-1:
                    cross[1] = blf[neighbor[0]][neighbor[1]][0]
                if cross in border:
                    crossings += 1
                    total += 1
            blf[i][j][1] = crossings
            crossings = 0
            cross = []
    if total != 0:
        for i in range(dim):
            for j in range(dim):
                blf[i][j][1] /= total
    return blf
            

def moving_target_search(env, blf, dim, rule, action):
    counter = 1
    i = 0
    j = 0
    found = 0
    while not found:
        blf[i][j][0] = env[i][j][0]
        rng = random.randint(1, 10)
        if blf[i][j][0] == 1:
            if rng > 1:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_flat
        if blf[i][j][0] == 2:
            if rng > 3:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_hilly
        if blf[i][j][0] == 3:
            if rng > 7:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_forest
        if blf[i][j][0] == 4:
            if rng > 9:
                if env[i][j][1] == 1:
                    found = 1
                    break
            blf[i][j][1] *= p_maze
        env, border = move_target(env, dim)
        blf = update_blf_mv(blf, dim, border)
##        print()
##        print("New belief table:")
##        for row in blf:
##            print(' '.join([str(elem) for elem in row]))
        coord = next_cell(blf, i, j, dim, rule, action)
        i = coord[0]
        j = coord[1]
        counter += 1
    return [counter, j, i]
        
## With print statements

##def search(env, blf, dim, rule, action):
##    counter = 1
##    i = 0
##    j = 0
##    found = 0
##    while not found:
##        print()
##        print("current is " + str(i) + ", " + str(j))
##        for row in blf:
##            print(' '.join([str(elem) for elem in row]))
##        blf[i][j][0] = env[i][j][0]
##        old_blf = blf[i][j][1]
##        rng = random.randint(1, 10)
##        if blf[i][j][0] == 1:
##            if rng > 1:
##                if env[i][j][1] == 1:
##                    found = 1
##                    break
##            blf[i][j][1] *= p_flat
##        if blf[i][j][0] == 2:
##            if rng > 3:
##                if env[i][j][1] == 1:
##                    found = 1
##                    break
##            blf[i][j][1] *= p_hilly
##        if blf[i][j][0] == 3:
##            if rng > 7:
##                if env[i][j][1] == 1:
##                    found = 1
##                    break
##            blf[i][j][1] *= p_forest
##        if blf[i][j][0] == 4:
##            if rng > 9:
##                if env[i][j][1] == 1:
##                    found = 1
##                    break
##            blf[i][j][1] *= p_maze
##        print("target not found at " + str(i) + ", " + str(j))
##        blf = update_blf(blf, i, j, old_blf, dim)
##        for row in blf:
##            print(' '.join([str(elem) for elem in row]))
##        coord = next_cell(blf, i, j, dim, rule, action)
##        print("next is " + str(coord[0]) + ", " + str(coord[1]))
##        i = coord[0]
##        j = coord[1]
##        counter += 1
##    print()
##    print("final belief grid:")
##    for row in blf:
##        print(' '.join([str(elem) for elem in row]))
##    return [counter, j, i]

dim = 50
trials = 1
rule = 0
action = 1
moving = 1
env = grid(dim)

##print()
##print("Rule 1 Trials:")
##rule_one = []
##for x in range(trials):
##    blf = blf_grid(dim, moving)
##    result = search(env, blf, dim, rule, action)
##    rule_one.append(result[0])
##    print()
##    print("Trial " + str(x) + ": It took " + str(result[0]) + " iteration(s) to find the target at (" + str(result[1]) + ", " + str(result[2]) + ")")
##print()
##print("Average is " + str(statistics.mean(rule_one)))
##print()
##
##rule = 1
##action = 1
##moving = 1
##print()
##print("Rule 2 Trials:")
##rule_two = []
##for y in range(trials):
##    blf = blf_grid(dim, moving)
##    result = search(env, blf, dim, rule, action)
##    rule_two.append(result[0])
##    print()
##    print("Trial " + str(y) + ": It took " + str(result[0]) + " iteration(s) to find the target at (" + str(result[1]) + ", " + str(result[2]) + ")")
##print()
##print("Average is " + str(statistics.mean(rule_two)))

print()
print("Moving Target, Rule 1")
res = []
for x in range(trials):
    blf = blf_grid(dim, moving)
    result = moving_target_search(env, blf, dim, rule, action)
    res.append(result[0])
    print()
    print("Trial " + str(x+1) + ": It took " + str(result[0]) + " iteration(s) to find the target at (" + str(result[1]) + ", " + str(result[2]) + ")")
print()
print("Average is " + str(statistics.mean(res)))

rule = 1
print()
print("Moving Target, Rule 2")
res = []
for x in range(trials):
    blf = blf_grid(dim, moving)
    result = moving_target_search(env, blf, dim, rule, action)
    res.append(result[0])
    print()
    print("Trial " + str(x+1) + ": It took " + str(result[0]) + " iteration(s) to find the target at (" + str(result[1]) + ", " + str(result[2]) + ")")
print()
print("Average is " + str(statistics.mean(res)))
