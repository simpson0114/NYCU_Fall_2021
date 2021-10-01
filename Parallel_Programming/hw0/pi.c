#include <stdio.h>
#include <stdlib.h>
#include <time.h>

long long int number_in_circle, number_of_tosses;
double x, y, distance_squared, pi_estimate;

int main(int argc, char *argv) {
    number_in_circle = 0;
    // number_of_tosses = 9223372036854775807;
    number_of_tosses = 10000000;
    srand(time(NULL));
    for (long long int toss = 0; toss < number_of_tosses; toss ++) {
        x = ((double)rand() - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        y = ((double)rand() - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        distance_squared = x * x + y * y;
        if ( distance_squared < 1 || distance_squared == 1)
            number_in_circle++;
    }
    pi_estimate = 4 * number_in_circle /(( double ) number_of_tosses);
    printf("%lf\n", pi_estimate);
}