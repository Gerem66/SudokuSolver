#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time

# Récupérer la grille
grille = []
for i in range(9):
    line = input(str(i) + '>>').split()
    grille.append(line)

# Fonctions
def FillCase(x, y):
    changed = False
    possibility = list(range(1, 10))
    # Each number
    # Line
    for _x in range(9):
        if grille[y][_x] != '?' and int(grille[y][_x]) in possibility:
            possibility.remove(int(grille[y][_x]))
    # Column
    for _y in range(9):
        if grille[_y][x] != '?' and int(grille[_y][x]) in possibility:
            possibility.remove(int(grille[_y][x]))
    # Case
    baseX = int(x / 3) * 3
    baseY = int(y / 3) * 3
    for _x in range(baseX, baseX + 3):
        for _y in range(baseY, baseY + 3):
            if grille[_y][_x] != '?' and int(grille[_y][_x]) in possibility:
                possibility.remove(int(grille[_y][_x]))

    #print(len(possibility))
    if len(possibility) == 1:
        grille[y][x] = str(possibility[0])
        changed = True

    return changed

def ReverseFill():
    changed = False
    # Pour chaque grosse case (3x3)
    for caseX in range(3):
        for caseY in range(3):
            # On prend chaque nombre
            for number in range(1, 10):
                # Et on le teste dans toute la grande case
                isOk = False
                for smallCaseX in range(3):
                    for smallCaseY in range(3):
                        if grille[smallCaseY][smallCaseX] != '?' and int(grille[_y][_x]) in possibility:
                            possibility.remove(int(grille[_y][_x]))
                        
    return changed

def IsSolved():
    solved = True
    for i in range(8):
        if '?' in grille[i]:
            solved = False
            break
    return solved

# Résolution de la grille
t_start = time()
while not IsSolved():
    changed = False
    for index in range(81):
        x = int(index % 9)
        y = int(index / 9)
        if grille[y][x] == '?':
            c = FillCase(x, y)
            if not changed and c:
                changed = True
    if not changed:
        ReverseFill()
t_end = time()

# Affichage du résultat
print("Temps mis : {} secondes".format(t_end - t_start))
print("Grille complétée :")
for index in range(81):
    x = int(index % 9)
    y = int(index / 9)
    if x == 0: print()
    print(grille[y][x], end=' ')