#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

 Colonne
    |     Region (Zone de 9 cases)
    |        |      Case (Nombre ou indices*)
    V        |       |
 +-------+---|---+---|---+
 | 1 2 3 |   |   | ? V ? |
 | 4 5 6 |   V   | ? ? ? | <-- Ligne
 | 7 8 9 |       | ? ? ? |
 +-------+-------+-------+
 |       |       |       |
 |       |       |       |
 |       |       |       |
 +-------+-------+-------+
 |       |       |       |
 |       |       |       |
 |       |       |       |
 +-------+-------+-------+

indices* = liste nombres possibles

'''

from time import time

def GetGrid():
    g = []
    for i in range(9):
        line = input().split()
        g.append(line)

    # Ajout de toutes les possibilités (? => 1-9)
    for x in range(9):
        for y in range(9):
            if g[y][x] == '?':
                g[y][x] = [str(i) for i in range(1, 10)]
    return g

def PrintGrid():
    for y in range(9):
        print(' '.join(grid[y]))

def IsFilled(x, y):
    return type(grid[y][x]) != list

def Solved():
    for x in range(9):
        for y in range(9):
            if not IsFilled(x, y):
                return False
    return True

def RemoveIndice(x, y, nb):
    changed = False
    grid[y][x].remove(nb)
    if len(grid[y][x]) == 1:
        grid[y][x] = grid[y][x][0]
        changed = True
    return changed

def ForceIndice(x, y, nb):
    grid[y][x] = nb

def FillCase(x, y):
    changed = False
    # On vérifie si les éléments de la liste des indices est déjà dans la ligne
    for _x in range(9):
        if x == _x or IsFilled(x, y): continue
        if IsFilled(_x, y) and grid[y][_x] in grid[y][x]:
            changed = RemoveIndice(x, y, grid[y][_x]) or changed

    # On vérifie si les éléments de la liste des indices est déjà dans la colonne
    if not IsFilled(x, y):
        for _y in range(9):
            if y == _y or IsFilled(x, y): continue
            if IsFilled(x, _y) and grid[_y][x] in grid[y][x]:
                changed = RemoveIndice(x, y, grid[_y][x]) or changed

    # On vérifie si les éléments de la liste des indices est déjà dans la région
    if not IsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        for _x in range(regionX, regionX + 3):
            for _y in range(regionY, regionY + 3):
                if (x == _x and y == _y) or IsFilled(x, y): continue
                if IsFilled(_x, _y) and grid[_y][_x] in grid[y][x]:
                    changed = RemoveIndice(x, y, grid[_y][_x]) or changed

    return changed

def ReduceIndices(x, y):
    changed = False

    # On vérifie si un des indices est seul sur une ligne
    if not IsFilled(x, y):
        for indice in grid[y][x]:
            isOK = True
            for _x in range(9):
                if _x == x: continue
                if IsFilled(_x, y):
                    if indice == grid[y][_x]:
                        isOK = False
                else:
                    if indice in grid[y][_x]:
                        isOK = False
            if isOK:
                ForceIndice(x, y, indice)
                changed = True
                break

    # On vérifie si un des indices est seul sur une colonne
    if not IsFilled(x, y):
        for indice in grid[y][x]:
            isOK = True
            for _y in range(9):
                if _y == y: continue
                if IsFilled(x, _y):
                    if indice == grid[_y][x]:
                        isOK = False
                else:
                    if indice in grid[_y][x]:
                        isOK = False
            if isOK:
                ForceIndice(x, y, indice)
                changed = True
                break

    # On vérifie si un des indices est seul dans une case (pas sûr que ce soit utile)
    if not IsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        for indice in grid[y][x]:
            isOK = True
            for _x in range(regionX, regionX + 3):
                for _y in range(regionY, regionY + 3):
                    if x == _x and y == _y: continue
                    if not IsFilled(_x, _y) and indice in grid[_y][_x]:
                        isOK = False
            if isOK:
                ForceIndice(x, y, indice)
                changed = True
                break

    # Vérifier si un même indice est aligné dans une case
    # Si il n'est que sur une des ligne d'une région, on peut le supprimer du reste de la ligne
    # Idem pour les colonnes
    if not IsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        # Dans chaque grosse case
        for indice in grid[y][x]:
            # Pour chaque valeur (1-9)
            state = 0
            linesUsed = []
            columnsUsed = []
            for smallCase in range(9):
                smallX = regionX + int(smallCase % 3)
                smallY = regionY + int(smallCase / 3)
                if IsFilled(smallX, smallY): continue
                if not IsFilled(smallX, smallY) and indice in grid[smallY][smallX]:
                    if not smallX in columnsUsed: columnsUsed.append(smallX)
                    if not smallY in linesUsed: linesUsed.append(smallY)
            if len(linesUsed) == 1:
                for _x in range(9):
                    if _x >= regionX and _x < regionX+3: continue
                    if not IsFilled(_x, linesUsed[0]) and indice in grid[linesUsed[0]][_x]:
                        changed = RemoveIndice(_x, linesUsed[0], indice) or changed
            if len(columnsUsed) == 1:
                for _y in range(9):
                    if _y >= regionY and _y < regionY+3: continue
                    if not IsFilled(columnsUsed[0], _y) and indice in grid[_y][columnsUsed[0]]:
                        changed = RemoveIndice(columnsUsed[0], _y, indice) or changed

    return changed

###########################
# Résolution de la grille #
###########################

grid = GetGrid()
grid_stable = None

t_start = time()
while not Solved():
    changed = False
    for y in range(9):
        for x in range(9):
            if not IsFilled(x, y):
                changed = FillCase(x, y) or changed
    if not changed:
        for index in range(81):
            x = int(index % 9)
            y = int(index / 9)
            if not IsFilled(x, y):
                if ReduceIndices(x, y):
                    changed = True
                    break
    if not changed:
        if grid_stable == None:
            # 1ère étape du choix
            # Recherche d'un élément contenant 2 indices
            for index in range(81):
                x = int(index % 9)
                y = int(index / 9)
                if not IsFilled(x, y) and len(grid[y][x]) == 2:
                    n1, n2 = grid[y][x]
                    grid[y][x] = n2 # On sauvegarde la liste en gardant le 2e indice
                    grid_stable = list(grid) # Copie de la grille
                    grid[y][x] = n1 # On choisi le 1er indice
                    break # On continue
            if grid_stable != None:
                continue
        else:
            # 2e étape
            # 1er choix ne mène nulle part, on choisi alors le 2nd indice
            grid = list(grid_stable)
            continue

    if not changed:
        print("Résolution échouée")
        exit()
t_end = time()

# Affichage du résultat
total_time = t_end - t_start
print("Grille résolue en {} secondes".format(total_time))
PrintGrid()