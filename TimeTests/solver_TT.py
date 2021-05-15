#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
'''
n = 100
grid = "easy_grid.txt" # easy_grid.txt | hard_grid.txt
for i in range(n):
    os.system("../solver < " + grid)
'''

# On récupère toutes les grilles
# Et on les stocke dans des fichiers
f = open('TimeTests/multi_grid.txt', 'r')
lines = f.readlines()
number_of_grid = int(len(lines) / 10)
f.close()

# On créer un fichier par grille
for i in range(number_of_grid):
    grid = lines[i*10+1:i*10+10]
    with open('multi_grid_' + str(i), 'w') as f:
        for g in grid:
            f.write(g.replace('0', '?'))

# On exécute le tout
t_start = time.time()
for i in range(number_of_grid):
    os.system('./solver < multi_grid_' + str(i))
    #os.system('./solver < multi_grid_' + str(i) + ' > multi_grid_solved_' + str(i))
t_end = time.time()

# On supprime les grilles créées précédemment
for i in range(number_of_grid):
    os.remove('multi_grid_' + str(i))
    #os.remove('multi_grid_solved_' + str(i))

t_total = round(t_end - t_start, 4)
t_avrg = round(t_total / number_of_grid, 4)
print('{} grilles résolues en {} secondes, soit {} secondes par grille en moyenne'.format(number_of_grid, t_total, t_avrg))