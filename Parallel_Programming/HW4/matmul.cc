#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

inline void read(char &x)
{
	x = 0;
    char c = getchar();
	while(c < '0' || c > '9')
        c = getchar();
	while(c >= '0' && c <= '9') {
		x = x * 10 + c - '0';
		c = getchar();
	} 
}

double time1, time2;

void construct_matrices(int *n_ptr, int *m_ptr, int *l_ptr, int **a_mat_ptr, int **b_mat_ptr){
	int world_rank, world_size, as, bs, i;
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &world_size);
	if(world_size == 5) {
		// double start_time = MPI_Wtime();
		int len, start, end;
		MPI_Request request[3];
		MPI_Request senda_req[5];
		
		if(world_rank == 0) {
			scanf("%d %d %d", n_ptr, m_ptr, l_ptr);
			for(i = 1; i < world_size; i++) {
				MPI_Isend(n_ptr, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &request[0]);
				MPI_Isend(m_ptr, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &request[1]);
				MPI_Isend(l_ptr, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &request[2]);
				MPI_Waitall(3, request, MPI_STATUSES_IGNORE);
			}
		}

		if(world_rank > 0) {
			MPI_Irecv( n_ptr , 1 , MPI_INT , 0 , 0 , MPI_COMM_WORLD , &request[0]);
			MPI_Irecv( m_ptr , 1 , MPI_INT , 0 , 0 , MPI_COMM_WORLD , &request[1]);
			MPI_Irecv( l_ptr , 1 , MPI_INT , 0 , 0 , MPI_COMM_WORLD , &request[2]);
			MPI_Waitall(3, request, MPI_STATUSES_IGNORE);
		}

		char *a_mat_ptr_char;
		char *b_mat_ptr_char;

		start = (*n_ptr / world_size) * world_rank;
		if (world_rank == world_size - 1)
			end = *n_ptr;
		else
			end = start + (*n_ptr / world_size);	
		len = (end - start) * (*m_ptr);
		
		as = (*n_ptr) * (*m_ptr);
		bs = (*m_ptr) * (*l_ptr);
		if(world_rank == 0)
			a_mat_ptr_char = new char [as];
		else
			a_mat_ptr_char = new char [len];
		b_mat_ptr_char = new char [bs];

		if(world_rank == 0) {
			int i, j, idx;
			for(i = 0 ; i < as ; i++){
				//scanf("%d", *a_mat_ptr+i);
				read(*(a_mat_ptr_char + i));
			}
			for(i = 0 ; i < *m_ptr ; i++){
				for(j = 0 ; j < *l_ptr ; j++){
					//scanf("%d", *b_mat_ptr+i+j*(*m_ptr));
					read(*(b_mat_ptr_char + i + j * (*m_ptr)));
				}
			}
		}
		

		// MPI_Bcast(*a_mat_ptr, as, MPI_INT, 0, MPI_COMM_WORLD);
		// MPI_Bcast(*b_mat_ptr, bs, MPI_INT, 0, MPI_COMM_WORLD);



		if(world_rank == 0) {
			for(i = 2; i < world_size; i += 2) {
				MPI_Isend(b_mat_ptr_char, bs, MPI_CHAR, i, 0, MPI_COMM_WORLD, &request[i/2]);
			}
			MPI_Waitall(world_size / 2, request, MPI_STATUSES_IGNORE);
		}
		if(world_rank % 2 == 0){
			if(world_rank != 0) {
				MPI_Irecv( b_mat_ptr_char, bs, MPI_CHAR , 0 , 0 , MPI_COMM_WORLD , &request[1]);
				MPI_Wait(&request[1], MPI_STATUSES_IGNORE);
				MPI_Isend(b_mat_ptr_char, bs, MPI_CHAR, world_rank - 1, 0, MPI_COMM_WORLD, &request[1]);
				MPI_Wait(&request[1], MPI_STATUSES_IGNORE);
			}
		}
		else {
			MPI_Irecv( b_mat_ptr_char, bs, MPI_CHAR , world_rank + 1 , 0 , MPI_COMM_WORLD , &request[1]);
			MPI_Wait(&request[1], MPI_STATUSES_IGNORE);
		}

		if(world_rank == 0) {
			for(i = 1; i < world_size; i ++) {
				start = (*n_ptr / world_size) * i;
				if (i == world_size - 1)
					end = *n_ptr;
				else
					end = start + (*n_ptr / world_size);	
				len = (end - start) * (*m_ptr);
				MPI_Isend(a_mat_ptr_char + start * (*m_ptr), len, MPI_CHAR, i, 0, MPI_COMM_WORLD, &senda_req[i-1]);
			}
			MPI_Waitall(world_size - 1, senda_req, MPI_STATUSES_IGNORE);
		}
		else {
			MPI_Irecv( a_mat_ptr_char, len, MPI_CHAR , 0 , 0 , MPI_COMM_WORLD , &request[2]);
			MPI_Wait( &request[2] , MPI_STATUSES_IGNORE);
		}
		*a_mat_ptr = (int *)a_mat_ptr_char;
		*b_mat_ptr = (int *)b_mat_ptr_char;
		// double end_time = MPI_Wtime();
		// time1 = end_time - start_time;
	}
	else if(world_rank == 0) {
		scanf("%d %d %d", n_ptr, m_ptr, l_ptr);
	
		as = (*n_ptr) * (*m_ptr);
		bs = (*m_ptr) * (*l_ptr);
		
		char *a_mat_ptr_char = new char [as];
		char *b_mat_ptr_char = new char [bs];
		int i, j;
		for(i = 0 ; i < as ; i++){
			//scanf("%d", *a_mat_ptr+i);
			read(*(a_mat_ptr_char + i));
		}
		for(i = 0 ; i < *m_ptr ; i++){
			for(j = 0 ; j < *l_ptr ; j++){
				//scanf("%d", *b_mat_ptr+i+j*(*m_ptr));
				read(*(b_mat_ptr_char + i + j * (*m_ptr)));
			}
		}
		*a_mat_ptr = (int *)a_mat_ptr_char;
		*b_mat_ptr = (int *)b_mat_ptr_char;
	}
}


void matrix_multiply(const int n, const int m, const int l, const int *a_mat, const int *b_mat){
	int world_rank, world_size;
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &world_size);
	if(world_size == 5) {
		// double start_time = MPI_Wtime();
		int len, start, end;
		len = n * l;
		start = (n / world_size) * world_rank;
		if (world_rank == world_size - 1)
			end = n;
		else
			end = start + (n / world_size);

		int *C = new int [len];
		char *a_mat_char = (char *)a_mat;
		char *b_mat_char = (char *)b_mat;
		
		int sum, i, j, k, a_idx, b_idx, c_idx;//, tmp, tc;
		//c_idx = start*l;
		a_idx = 0;
		
		for(i = start ; i < end ; i++, a_idx += m){
			c_idx = i * l;
			//a_idx = i*m;
			//tc = c_idx;
			b_idx = 0;
			for(j = 0 ; j < l ; j++){
				sum = 0;
				for(k = 0 ; k < m ; k++){
					sum += (int)a_mat_char[a_idx+k] * b_mat_char[b_idx];
					//sum += tmp;
					b_idx++;
				}
				C[c_idx] = sum;
				c_idx++;
				//C[tc] = sum;
				//tc++;
			}
		}
		if(world_rank > 0)
		{
			MPI_Send(C + start * l, (end - start) * l, MPI_INT, 0, 0, MPI_COMM_WORLD);
		}

		if(world_rank == 0){
			MPI_Request requests[world_size-1];
			
			for (int source = 1; source < world_size; source++)
			{
				start = (n / world_size) * source;
				if (source == world_size - 1)
					end = n;
				else
					end = start + (n / world_size);
				MPI_Irecv( C + start * l, (end - start) * l, MPI_INT, source, 0, MPI_COMM_WORLD, &requests[source-1]);
			}
			MPI_Waitall(world_size-1, requests, MPI_STATUSES_IGNORE);
			for(i = 0 ; i < n ; i++){
				c_idx = i * l;
				for(j = 0 ; j < l ; j++){
					printf("%d", C[c_idx]);
					putchar(' ');
					c_idx++;
				}
				putchar('\n');
			}
		}
		// double end_time = MPI_Wtime();
		// time2 = end_time - start_time;
	}
	else if(world_rank == 0) {
		int len, start, end;
		len = n * l;
		int *C = new int [len];
		char *a_mat_char = (char *)a_mat;
		char *b_mat_char = (char *)b_mat;
		int sum, i, j, k, a_idx, b_idx, c_idx;//, tmp, tc;
		c_idx = 0;
		a_idx = 0;
	
		for(i = 0 ; i < n ; i++, a_idx += m){
			c_idx = i * l;
			//a_idx = i*m;
			//tc = c_idx;
			b_idx = 0;
			for(j = 0 ; j < l ; j++){
				sum = 0;
				for(k = 0 ; k < m ; k++){
					sum += (int)a_mat_char[a_idx+k] * b_mat_char[b_idx];
					//sum += tmp;
					b_idx++;
				}
				C[c_idx] = sum;
				c_idx++;
				//C[tc] = sum;
				//tc++;
			}
		}

		for(i = 0 ; i < n ; i++){
			c_idx = i * l;
			for(j = 0 ; j < l ; j++){
				printf("%d", C[c_idx]);
				putchar(' ');
				c_idx++;
			}
			//printf("\n");
			putchar('\n');
		}
	}
}

void destruct_matrices(int *a_mat, int *b_mat){
	int world_rank;
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
	if(world_rank == 0){
		free(a_mat);
		free(b_mat);
	}
	// printf("%lf\n", time1);
	// printf("%lf\n", time2);
}