#include <stdio.h>
#include <stdlib.h>

int main()
{
    void *avoid_consolidation;
    void *unsorted_bin;

    unsorted_bin = malloc(0x410);   // info 0x10 + data 0x410
    avoid_consolidation = malloc(0x10);

    free(unsorted_bin);
    malloc(0x3f0);
    malloc(0x20); // 0x30 > 0x20, 0x20 unsorted bin --> 0x20 smallbin

    return 0;
}