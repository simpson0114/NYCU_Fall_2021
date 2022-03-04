#include <stdio.h>
#include <stdlib.h>

int main() {
    char *A = (char *) malloc(0x1a);
    char *B = (char *) malloc(0x12);
    char *C = (char *) malloc(0x14);
    char *D = (char *) malloc(0x16);
    char *E = (char *) malloc(0x30);
    char *F = (char *) malloc(0x16);
    char *G = (char *) malloc(0x29);
    free(F);
    free(B);
    free(G);
    free(D);
    free(A);
    free(E);
    free(C);
    unsigned long *X = (unsigned long *) malloc(0x50);
    unsigned long *Y = (unsigned long *) malloc(0x50);
    Y[1] = 0xdeadbeef;
    return 0;
}