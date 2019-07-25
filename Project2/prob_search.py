import random

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
    target = random.randint(1, dim*dim)
    env[int(target/dim)][target%dim][1] = 1
    ##for row in env:
    ##    print(' '.join([str(elem) for elem in row]))
    return env

## Each cell in the belief grid initially takes the form [type, probability], where type for all is unknown (0)
## and the probability is 1/(# of cells)
def blf_grid(dim):
    blf = [[[0, 1/(dim*dim)]] * dim for i in range(dim)]
    ##for row in blf:
    ##    print(' '.join([str(elem) for elem in row]))
    return blf

def next_cell(blf, dim):
    max = 0
    coord = [0, 0]
    for i in range(dim):
        for j in range(dim):
            if blf[i][j][1] > max:
                max = blf[i][j][1]
                coord = [i, j]
    return coord
 
def search(env, blf, dim):
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
        if blf[i][j][0] == 2:
            if rng > 3:
                if env[i][j][1] == 1:
                    found = 1
                    break
        if blf[i][j][0] == 3:
            if rng > 7:
                if env[i][j][1] == 1:
                    found = 1
                    break
        if blf[i][j][0] == 4:
            if rng > 9:
                if env[i][j][1] == 1:
                    found = 1
                    break
        next = next_cell(blf, dim)
        i = next[0]
        j = next[1]
        

env = grid(10)
blf = blf_grid(10)
