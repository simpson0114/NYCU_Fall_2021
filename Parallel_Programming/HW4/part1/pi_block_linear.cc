#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>

long int Cal_Pi(long int local_toss);

int main(int argc, char **argv)
{
    // --- DON'T TOUCH ---
    MPI_Init(&argc, &argv);
    double start_time = MPI_Wtime();
    double pi_result;
    long int tosses = atoi(argv[1]);
    int world_rank, world_size;
    // ---
    
    // TODO: init MPI
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    int tag = 0;
    int dest = 0;
    long int total = 0;
    MPI_Status status;
    srand(world_rank*time(NULL));
    long int  local_toss = tosses / world_size;
    long int  local_num = Cal_Pi(local_toss);

    if (world_rank > 0)
    {
        // TODO: handle workers
        MPI_Send(&local_num, 1, MPI_LONG, dest, tag, MPI_COMM_WORLD);
    }
    else if (world_rank == 0)
    {
        // TODO: master
        total = local_num;
        for (int source = 1; source < world_size; source++)
        {
            MPI_Recv( &local_num, 1, MPI_LONG, source, tag, MPI_COMM_WORLD, &status);
            total = total + local_num;
        }
    }

    if (world_rank == 0)
    {
        // TODO: process PI result
        pi_result = 4 * total /(( double ) tosses);

        // --- DON'T TOUCH ---
        double end_time = MPI_Wtime();
        printf("%lf\n", pi_result);
        printf("MPI running time: %lf Seconds\n", end_time - start_time);
        // ---
    }

    MPI_Finalize();
    return 0;
}

long int Cal_Pi(long int  local_toss) {
    long int  number_in_circle = 0;
    for (long int  toss = 0; toss < local_toss; toss ++) {
        double x = ((double)rand() - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        double y = ((double)rand() - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
        double distance_squared = x * x + y * y;
        if ( distance_squared < 1 || distance_squared == 1)
            number_in_circle++;
    }
    return number_in_circle;
}