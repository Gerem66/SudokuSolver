#include <stdio.h>

void PrintGrid(int *grid[9][9]) {
    for (int y = 0; y < 9; y++) {
        for (int x = 0; x < 9; x++) {
            printf("%d ", grid[y][x][0]);
        }
        printf("\n");
    }
}

int main(void) {
    int *grid[9][9];
    for (int y = 0; y < 9; y++) {
        for (int x = 0; x < 9; x++) {
            for (int i = 0; i < 9; i++) {
                if (i == 0) {
                    int value = 5;
                    grid[y][x] = &value;
                } else {
                    int v = 4;
                    grid[y][x] = &v;
                }
                //else grid[y][x] = 0;
            }
        }
    }
    //printf("%d\n", grid[0][0][4]);
    PrintGrid(grid);
    printf("Hello world !\n");
    return 0;
}








/*
#include <stdio.h>

void PrintGrid(int (*grid)[9][9][9]) {
    for (int y = 0; y < 9; y++) {
        for (int x = 0; x < 9; x++) {
            printf("%d ", (*grid)[y][x][0]);
        }
        printf("\n");
    }
}

int main(void) {
    int grid[9][9][9];
    for (int y = 0; y < 9; y++) {
        for (int x = 0; x < 9; x++) {
            for (int i = 0; i < 9; i++) {
                if (i == 0) grid[y][x][i] = x + y;
                else grid[y][x][i] = 0;
            }
        }
    }
    //printf("%d\n", grid[0][0][4]);
    PrintGrid(&grid);
    printf("Hello world !\n");
    return 0;
}
*/