#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>

long long int Cal_Pi(long long int local_toss);

int fnz(long long int *num, int world_size) {
    for(int i = 0; i < world_size; i++) {
        if(num[i] == 0)
            return 0;
    }
    return 1;
}

int main(int argc, char **argv)
{
    // --- DON'T TOUCH ---
    MPI_Init(&argc, &argv);
    double total_time = 0;
    for(int i = 0; i < 10; i++) {
        double start_time = MPI_Wtime();
        double pi_result;
        long long int tosses = atoi(argv[1]);
        int world_rank, world_size;
        // ---

        MPI_Win win;

        // TODO: MPI init
        MPI_Comm_size(MPI_COMM_WORLD, &world_size);
        MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

        srand(world_rank*time(NULL));
        long long int total = 0;
        long long int local_toss = tosses / world_size;
        long long int local_num = Cal_Pi(local_toss);
        if (world_rank == 0)
        {
            // Master
            long long int *num;
            MPI_Alloc_mem((world_size - 1) * sizeof(long long int), MPI_INFO_NULL, &num);

            for (int i = 0; i < world_size - 1; i++)
                num[i] = 0;

            MPI_Win_create(num, (world_size - 1) * sizeof(long long int), sizeof(long long int), MPI_INFO_NULL,
            MPI_COMM_WORLD, &win);

            int ready = 0;
            while (!ready)
            {
                // Without the lock/unlock schedule stays forever filled with 0s
                MPI_Win_lock(MPI_LOCK_SHARED, 0, 0, win);
                ready = fnz(num, world_size - 1);
                MPI_Win_unlock(0, win);
            }

            total = local_num;
            for(int i = 0; i < world_size - 1; i++)
                total += num[i];
            
            MPI_Win_free(&win);
            MPI_Free_mem(num);
        }
        else
        {
            // Workers
            MPI_Win_create(NULL, 0, 1, MPI_INFO_NULL, MPI_COMM_WORLD, &win);

            MPI_Win_lock(MPI_LOCK_EXCLUSIVE, 0, 0, win);
            MPI_Put(&local_num, 1, MPI_LONG_LONG_INT, 0, world_rank - 1, 1, MPI_LONG_LONG_INT, win);
            MPI_Win_unlock(0, win);

            MPI_Win_free(&win);
        }

        if (world_rank == 0)
        {
            // TODO: handle PI result
            pi_result = 4 * total /(( double ) tosses);
            
            // --- DON'T TOUCH ---
            double end_time = MPI_Wtime();
            // printf("%lf\n", pi_result);
            // printf("MPI running time: %lf Seconds\n", end_time - start_time);
            double time = end_time - start_time;
            if(total_time != 0 && abs(time - total_time/(i+1)) > 1) {
                printf("Run it again!\n");
                total_time += end_time - start_time;
            }
            else
                total_time += end_time - start_time;

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