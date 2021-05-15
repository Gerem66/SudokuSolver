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

# Récupérer la grille
grille = []
for i in range(9):
    line = input().split()
    grille.append(line)

# Ajout de toutes les possibilités (? => 1-9)
for x in range(9):
    for y in range(9):
        if grille[y][x] == '?':
            grille[y][x] = [str(i) for i in range(1, 10)]

# Fonctions
def PrintGrille():
    for y in range(9):
        for x in range(9):
            print(grille[y][x], end=' ')
        print()

def IsFilled(x, y):
    return type(grille[y][x]) != list

def Solved():
    solved = True
    for x in range(9):
        for y in range(9):
            if not IsFilled(x, y):
                solved = False
    return solved

def RemoveIndice(x, y, nb):
    changed = False
    grille[y][x].remove(nb)
    if len(grille[y][x]) == 1:
        grille[y][x] = grille[y][x][0]
        changed = True
    return changed

def ForceIndice(x, y, nb):
    grille[y][x] = nb

def FillCase(x, y):
    changed = False
    # On vérifie si les éléments de la liste des indices est déjà dans la ligne
    for _x in range(9):
        if x == _x: continue
        if IsFilled(_x, y) and grille[y][_x] in grille[y][x]:
            changed = RemoveIndice(x, y, grille[y][_x]) or changed

    # On vérifie si les éléments de la liste des indices est déjà dans la colonne
    if not IsFilled(x, y):
        for _y in range(9):
            if y == _y: continue
            if IsFilled(x, _y) and grille[_y][x] in grille[y][x]:
                changed = RemoveIndice(x, y, grille[_y][x]) or changed

    # On vérifie si les éléments de la liste des indices est déjà dans la région
    if not IsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        for _x in range(regionX, regionX + 3):
            for _y in range(regionY, regionY + 3):
                if x == _x and y == _y: continue
                if IsFilled(_x, _y) and grille[_y][_x] in grille[y][x]:
                    changed = RemoveIndice(x, y, grille[_y][_x]) or changed
    
    # On vérifie si un des indices est seul sur une ligne
    if not IsFilled(x, y):
        for indice in grille[y][x]:
            isOK = True
            for _x in range(9):
                if _x == x: continue
                if IsFilled(_x, y):
                    if indice == grille[y][_x]:
                        isOK = False
                else:
                    if indice in grille[y][_x]:
                        isOK = False
            if isOK:
                ForceIndice(x, y, indice)
                changed = True
                break

    # On vérifie si un des indices est seul sur une colonne
    if not IsFilled(x, y):
        for indice in grille[y][x]:
            isOK = True
            for _y in range(9):
                if _y == y: continue
                if IsFilled(x, _y):
                    if indice == grille[_y][x]:
                        isOK = False
                else:
                    if indice in grille[_y][x]:
                        isOK = False
            if isOK:
                ForceIndice(x, y, indice)
                changed = True
                break
    
    # On vérifie si un des indices est seul dans une case (pas sûr que ce soit utile)
    if not IsFilled(x, y):
        regionX = int(x / 3) * 3
        regionY = int(y / 3) * 3
        for indice in grille[y][x]:
            isOK = True
            for _x in range(regionX, regionX + 3):
                for _y in range(regionY, regionY + 3):
                    if x == _x and y == _y: continue
                    if not IsFilled(_x, _y) and indice in grille[_y][_x]:
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
        for indice in grille[y][x]:
            # Pour chaque valeur (1-9)
            state = 0
            linesUsed = []
            columnsUsed = []
            for smallCase in range(9):
                smallX = regionX + int(smallCase % 3)
                smallY = regionY + int(smallCase / 3)
                if IsFilled(smallX, smallY): continue
                if not IsFilled(smallX, smallY) and str(indice) in grille[smallY][smallX]:
                    if not smallX in columnsUsed: columnsUsed.append(smallX)
                    if not smallY in linesUsed: linesUsed.append(smallY)
            if len(linesUsed) == 1:
                for _x in range(9):
                    if _x >= regionX and _x < regionX+3: continue
                    if not IsFilled(_x, linesUsed[0]) and str(indice) in grille[linesUsed[0]][_x]:
                        changed = RemoveIndice(_x, linesUsed[0], str(indice)) or changed
            if len(columnsUsed) == 1:
                for _y in range(9):
                    if _y >= regionY and _y < regionY+3: continue
                    if not IsFilled(columnsUsed[0], _y) and str(indice) in grille[_y][columnsUsed[0]]:
                        changed = RemoveIndice(columnsUsed[0], _y, str(indice)) or changed

    return changed

# Résolution de la grille
t_start = time()
attemps = 1000
while not Solved():
    changed = False
    for index in range(81):
        x = int(index % 9)
        y = int(index / 9)
        if not IsFilled(x, y):
            changed = FillCase(x, y) or changed
    if not changed:
        attemps -= 1
        if attemps <= 0:
            print("Bloqué")
            PrintGrille()
            exit()
t_end = time()

# Affichage du résultat
print("Temps mis : {} secondes".format(t_end - t_start))
print("Grille complétée :")
PrintGrille()