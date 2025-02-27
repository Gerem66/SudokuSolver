#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Pseudo  : Gerem
Discord : Terra#4811
Date    : 04/05/21
Dev en  : 2 jours

Temps d'exécution
    En moyenne sur des grilles de tout niveau   :  0.032 s
    Les grilles de niveau facile (min)          : 0.0006 s
    Les grilles les plus difficile (max)        :  > 0.2 s

Pour le vocabulaire
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

def GetGridFromStdin():
    g = []
    for i in range(9):
        line = input().split()
        g.append(line)

    # Ajout de toutes les possibilités (? => 1-9)
    poss = [str(i) for i in range(1, 10)]
    for x in range(9):
        for y in range(9):
            if g[y][x] == '?':
                g[y][x] = list(poss)
    return g

def PrintGrid():
    for y in range(9):
        print(' '.join(grid[y]))

def CaseIsFilled(x, y):
    return type(grid[y][x]) == str

def GridIsSolved():
    for x in range(9):
        for y in range(9):
            if not CaseIsFilled(x, y):
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
        if x == _x or CaseIsFilled(x, y): continue
        if CaseIsFilled(_x, y) and grid[y][_x] in grid[y][x]:
            changed = RemoveIndice(x, y, grid[y][_x]) or changed

    # On vérifie si les éléments de la liste des indices est déjà dans la colonne
    if not CaseIsFilled(x, y):
        for _y in range(9):
            if y == _y or CaseIsFilled(x, y): continue
            if CaseIsFilled(x, _y) and grid[_y][x] in grid[y][x]:
                changed = RemoveIndice(x, y, grid[_y][x]) or changed

    # On vérifie si les éléments de la liste des indices est déjà dans la région
    if not CaseIsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        for _x in range(regionX, regionX + 3):
            for _y in range(regionY, regionY + 3):
                if (x == _x and y == _y) or CaseIsFilled(x, y): continue
                if CaseIsFilled(_x, _y) and grid[_y][_x] in grid[y][x]:
                    changed = RemoveIndice(x, y, grid[_y][_x]) or changed

    return changed

def ReduceIndices(x, y):
    changed = False

    # On vérifie si un des indices est seul sur une ligne
    if not CaseIsFilled(x, y):
        for indice in grid[y][x]:
            isOK = True
            for _x in range(9):
                if _x == x: continue
                if CaseIsFilled(_x, y):
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
    if not CaseIsFilled(x, y):
        for indice in grid[y][x]:
            isOK = True
            for _y in range(9):
                if _y == y: continue
                if CaseIsFilled(x, _y):
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
    '''if not IsFilled(x, y):
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
                break'''

    # Vérifier si un même indice est aligné dans une case
    # Si il n'est que sur une des ligne d'une région, on peut le supprimer du reste de la ligne
    # Idem pour les colonnes
    if not CaseIsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        for indice in grid[y][x]:
            state = 0
            linesUsed = []
            columnsUsed = []
            for smallCase in range(9):
                smallX = regionX + int(smallCase % 3)
                smallY = regionY + int(smallCase / 3)
                if CaseIsFilled(smallX, smallY): continue
                if not CaseIsFilled(smallX, smallY) and indice in grid[smallY][smallX]:
                    if not smallX in columnsUsed: columnsUsed.append(smallX)
                    if not smallY in linesUsed: linesUsed.append(smallY)
            if len(linesUsed) == 1:
                for _x in range(9):
                    if _x >= regionX and _x < regionX+3: continue
                    if not CaseIsFilled(_x, linesUsed[0]) and indice in grid[linesUsed[0]][_x]:
                        changed = RemoveIndice(_x, linesUsed[0], indice) or changed
            if len(columnsUsed) == 1:
                for _y in range(9):
                    if _y >= regionY and _y < regionY+3: continue
                    if not CaseIsFilled(columnsUsed[0], _y) and indice in grid[_y][columnsUsed[0]]:
                        changed = RemoveIndice(columnsUsed[0], _y, indice) or changed

    return changed

###########################
# Résolution de la grille #
###########################

grid = GetGridFromStdin()
grid_stable = None

while not GridIsSolved():
    changed = False
    # 1ère étape
    # Remplissage des case évidentes
    for y in range(9):
        for x in range(9):
            if not CaseIsFilled(x, y):
                changed = FillCase(x, y) or changed
    # 2ème étape (si la 1ère ne suffit pas)
    # On réduit le nombre d'indices par cases
    if not changed:
        for index in range(81):
            x = int(index % 9)
            y = int(index / 9)
            if not CaseIsFilled(x, y):
                if ReduceIndices(x, y):
                    changed = True
    # 3ème étape (les 2 premières ne suffisent pas)
    # Si une case ne possède que 2 indices, un de ses deux est correct
    if not changed:
        if grid_stable == None:
            # Étape 3.1 : choix
            # Recherche d'un élément contenant 2 indices
            for index in range(81):
                x = int(index % 9)
                y = int(index / 9)
                if not CaseIsFilled(x, y) and len(grid[y][x]) == 2:
                    n1, n2 = grid[y][x]
                    grid[y][x] = n1             # On sauvegarde la liste en gardant le 2e indice
                    grid_stable = list(grid)    # Copie de la grille
                    grid[y][x] = n2             # On choisi le 1er indice
                    break                       # On continue la résolution
            if grid_stable != None:
                continue
        else:
            # Étape : 2e choix
            # Si le 1er choix ne mène nulle part, on choisi alors le 2nd indice
            grid = list(grid_stable)
            grid_stable = None
            continue

    # 4ème étape (RIP)
    if not changed:
        print("Résolution échouée")
        exit()

# Affichage du résultat
PrintGrid()