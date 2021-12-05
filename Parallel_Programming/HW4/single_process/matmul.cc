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

void construct_matrices(int *n_ptr, int *m_ptr, int *l_ptr, int **a_mat_ptr, int **b_mat_ptr){
	int world_rank, world_size, as, bs;
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

	if(world_rank == 0) {
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
	if(world_rank == 0) {
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
}