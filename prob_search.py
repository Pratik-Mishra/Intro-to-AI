import random


def grid(dim):
    env = [[0, 0] * dim for i in range(dim)]
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
    for row in env:
        print(' '.join([str(elem) for elem in row]))
    return env

grid(10)
