#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

int thread_count;
long long int number_in_circle = 0;
long long int number_of_tosses;
double pi_estimate;
pthread_mutex_t mutex;

void* Thread_sum(void * rank) {
    long int my_rank = (long int) rank;
    double factor;
    long long int i;
    long long int my_n = number_of_tosses / thread_count;
    long long int my_first_i = my_n*my_rank;
    long long int my_last_i = my_first_i + my_n;
    long long int my_sum = 0;
    double x, y, distance_squared;
    unsigned int seed = time(NULL);
    for (i = my_first_i; i < my_last_i; i++) {
        x = ((double)rand_r(&seed) - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        y = ((double)rand_r(&seed) - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        distance_squared = x * x + y * y;
        if (distance_squared <= 1)
            my_sum++;
    }
    pthread_mutex_lock(&mutex);
    number_in_circle += my_sum;
    pthread_mutex_unlock(&mutex);
    pthread_exit(NULL);
}  /* Thread_sum */

int main(int argc, char *argv[]) {
    long int thread;
    pthread_t * thread_handles;
    // number_of_tosses = 9223372036854775807;
    thread_count = strtol(argv[1], NULL, 10);
    number_of_tosses = strtoll(argv[2], NULL, 10);
    thread_handles = (pthread_t*) malloc (thread_count * sizeof(pthread_t));
    pthread_mutex_init(&mutex, NULL);

    for (thread = 0; thread < thread_count; thread++)  
        pthread_create(&thread_handles[thread], NULL, Thread_sum, (void*)thread);  
    for (thread = 0; thread < thread_count; thread++) 
        pthread_join(thread_handles[thread], NULL);

    
    pi_estimate = 4 * number_in_circle /(( double ) number_of_tosses);
    printf("%lf\n", pi_estimate);
    pthread_mutex_destroy(&mutex);
    free(thread_handles);
    return 0;
}