#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>

long long int Cal_Pi(long long int local_toss);

int main(int argc, char **argv)
{
    // --- DON'T TOUCH ---
    double total_time = 0;
    MPI_Init(&argc, &argv);
    for(int i = 0; i < 10; i++) {
        double start_time = MPI_Wtime();
        double pi_result;
        long long int tosses = atoi(argv[1]);
        int world_rank, world_size;
        // ---

        // TODO: MPI init
        MPI_Comm_size(MPI_COMM_WORLD, &world_size);
        MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

        int root_rank = 0;
        srand(world_rank*time(NULL));
        long long int total = 0;
        long long int local_toss = tosses / world_size;
        long long int local_num = Cal_Pi(local_toss);
        // TODO: use MPI_Gather
        if(world_rank == root_rank) {
            long long int global_num[world_size];
            MPI_Gather( &local_num , 1 , MPI_LONG_LONG_INT , global_num , 1 , MPI_LONG_LONG_INT , root_rank , MPI_COMM_WORLD);
            for(int rank = 0; rank < world_size; rank++)
                total += global_num[rank];
        }
        else
            MPI_Gather( &local_num , 1 , MPI_LONG_LONG_INT , NULL , 0 , MPI_LONG_LONG_INT , root_rank , MPI_COMM_WORLD);
        
        
        if (world_rank == 0)
        {
            // TODO: PI result
            pi_result = 4 * total /(( double ) tosses);

            // --- DON'T TOUCH ---
            double end_time = MPI_Wtime();
            // printf("%lf\n", pi_result);
            // printf("MPI running time: %lf Seconds\n", end_time - start_time);
            double time = end_time - start_time;
            if(total_time != 0 && abs(time - total_time/(i+1)) > 1) {
                total_time += end_time - start_time;
            }
            else
                total_time += end_time - start_time;
            printf("gather MPI running time: %lf Seconds\n", time);
            if(i == 9)
                printf("avg gather MPI running time: %lf Seconds\n", total_time / 10);
            // ---
        }
    }
    MPI_Finalize();
    return 0;
}

long long int Cal_Pi(long long int  local_toss) {
    long long int  number_in_circle = 0;
    for (long long int  toss = 0; toss < local_toss; toss ++) {
        double x = ((double)rand() - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        double y = ((double)rand() - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        double distance_squared = x * x + y * y;
        if ( distance_squared < 1 || distance_squared == 1)
            number_in_circle++;
    }
    return number_in_circle;
}