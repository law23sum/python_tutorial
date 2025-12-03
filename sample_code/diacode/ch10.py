#################chapter 10


import matplotlib.pyplot as plt
from matplotlib import collections as mc


def drawlattice(n, name):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            plt.plot(i, j, 'o', c='black')
    plt.savefig(name)


drawlattice(5, 'lattice.png')

game = [[(1, 2), (1, 1)], [(3, 3), (4, 3)], [(1, 5), (2, 5)], [(1, 2), (2, 2)], [(2, 2), (2, 1)], [(1, 1), (2, 1)], \
        [(3, 4), (3, 3)], [(3, 4), (4, 4)]]


def drawgame(n, name, game):
    colors2 = []
    for k in range(0, len(game)):
        if k % 2 == 0:
            colors2.append('red')
        else:
            colors2.append('blue')
    lc = mc.LineCollection(game, colors=colors2, linewidths=2)
    fig, ax = plt.subplots()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            plt.plot(i, j, 'o', c='black')
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.savefig(name)


drawgame(5, 'gameinprogress.png', game)


def squarefinder(game):
    countofsquares = 0
    for line in game:
        parallel = False
        left = False
        right = False
        if line[0][1] == line[1][1]:
            if [(line[0][0], line[0][1] - 1), (line[1][0], line[1][1] - 1)] in game:
                parallel = True
            if [(line[0][0], line[0][1]), (line[1][0] - 1, line[1][1] - 1)] in game:
                left = True
            if [(line[0][0] + 1, line[0][1]), (line[1][0], line[1][1] - 1)] in game:
                right = True
            if parallel and left and right:
                countofsquares += 1
    return (countofsquares)


def score(game):
    score = [0, 0]
    progress = []
    squares = 0
    for line in game:
        progress.append(line)
        newsquares = squarefinder(progress)
        if newsquares > squares:
            if len(progress) % 2 == 0:
                score[1] = score[1] + 1
            else:
                score[0] = score[0] + 1
        squares = newsquares
    return (score)


allpossible = []
gamesize = 5
for i in range(1, gamesize + 1):
    for j in range(2, gamesize + 1):
        allpossible.append([(i, j), (i, j - 1)])
for i in range(1, gamesize):
    for j in range(1, gamesize + 1):
        allpossible.append([(i, j), (i + 1, j)])

for move in allpossible:
    if move in game:
        allpossible.remove(move)

simple_tree = [[(4, 4), (4, 3)], [(1, 3), (2, 3)]]

simple_tree_with_children = [[[(4, 4), (4, 3)], []], [[(1, 3), (2, 3)], []]]

full_tree = [[[(4, 4), (4, 3)], [[(1, 3), (2, 3)], [(3, 1), (4, 1)]]], [[(1, 3), (2, 3)], [[(4, 4), (4, 3)], \
                                                                                           [(3, 1), (4, 1)]]]]


def generate_tree(possible_moves, depth, maxdepth):
    tree = []
    for move in possible_moves:
        move_profile = [move]
        if depth < maxdepth:
            possible_moves2 = possible_moves.copy()
            possible_moves2.remove(move)
            move_profile.append(generate_tree(possible_moves2, depth + 1, maxdepth))
        tree.append(move_profile)
    return (tree)


allpossible = [[(4, 4), (4, 3)], [(4, 1), (5, 1)]]
thetree = generate_tree(allpossible, 0, 1)
print(thetree)


def generate_tree(possible_moves, depth, maxdepth, game_so_far):
    tree = []
    for move in possible_moves:
        move_profile = [move]
        game2 = game_so_far.copy()
        game2.append(move)
        move_profile.append(score(game2))
        if depth < maxdepth:
            possible_moves2 = possible_moves.copy()
            possible_moves2.remove(move)
            move_profile.append(generate_tree(possible_moves2, depth + 1, maxdepth, game2))
        else:
            move_profile.append([])
        tree.append(move_profile)
    return (tree)


allpossible = [[(4, 4), (4, 3)], [(4, 1), (5, 1)]]
thetree = generate_tree(allpossible, 0, 1, [])
print(thetree)

import numpy as np


def minimax(max_or_min, tree):
    allscores = []
    for move_profile in tree:
        if move_profile[2] == []:
            allscores.append(move_profile[1][0] - move_profile[1][1])
        else:
            move, score = minimax((-1) * max_or_min, move_profile[2])
            allscores.append(score)
    newlist = [score * max_or_min for score in allscores]
    bestscore = max(newlist)
    bestmove = np.argmax(newlist)
    return (bestmove, max_or_min * bestscore)


allpossible = []
game = [[(1, 2), (1, 1)], [(3, 3), (4, 3)], [(1, 5), (2, 5)], [(1, 2), (2, 2)], [(2, 2), (2, 1)], [(1, 1), (2, 1)], \
        [(3, 4), (3, 3)], [(3, 4), (4, 4)]]
gamesize = 5

for i in range(1, gamesize + 1):
    for j in range(2, gamesize + 1):
        allpossible.append([(i, j), (i, j - 1)])

for i in range(1, gamesize):
    for j in range(1, gamesize + 1):
        allpossible.append([(i, j), (i + 1, j)])

for move in allpossible:
    if move in game:
        allpossible.remove(move)

thetree = generate_tree(allpossible, 0, 3, game)

move, score = minimax(1, thetree)

print(thetree[move][0])
