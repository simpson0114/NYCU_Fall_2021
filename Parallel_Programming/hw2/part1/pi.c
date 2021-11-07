#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <pthread.h>
#include <immintrin.h>

int thread_count;
long long int number_in_circle = 0;
long long int n, number_of_tosses;
double pi_estimate;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
__m256 ones, RND_MAX;


struct avx_xorshift128plus_key_s{
	__m256i part1;
	__m256i part2;
};

typedef struct avx_xorshift128plus_key_s avx_xorshift128plus_key_t;

static void xorshift128plus_onkeys(uint64_t * ps0, uint64_t * ps1) {
	uint64_t s1 = *ps0;
	const uint64_t s0 = *ps1;
	*ps0 = s0;
	s1 ^= s1 << 23; // a
	*ps1 = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5); // b, c
}

static void xorshift128plus_jump_onkeys(uint64_t in1, uint64_t in2,
		uint64_t * output1, uint64_t * output2) {
	static const uint64_t JUMP[] = { 0x8a5cd789635d2dff, 0x121fd2155c472f96 };
	uint64_t s0 = 0;
	uint64_t s1 = 0;
	for (unsigned int i = 0; i < sizeof(JUMP) / sizeof(*JUMP); i++)
		for (int b = 0; b < 64; b++) {
			if (JUMP[i] & 1ULL << b) {
				s0 ^= in1;
				s1 ^= in2;
			}
			xorshift128plus_onkeys(&in1, &in2);
		}
	output1[0] = s0;
	output2[0] = s1;
}

void avx_xorshift128plus_init(uint64_t key1, uint64_t key2,
		avx_xorshift128plus_key_t *key) {
	uint64_t S0[4];
	uint64_t S1[4];
	S0[0] = key1;
	S1[0] = key2;
	xorshift128plus_jump_onkeys(*S0, *S1, S0 + 1, S1 + 1);
	xorshift128plus_jump_onkeys(*(S0 + 1), *(S1 + 1), S0 + 2, S1 + 2);
	xorshift128plus_jump_onkeys(*(S0 + 2), *(S1 + 2), S0 + 3, S1 + 3);
	key->part1 = _mm256_loadu_si256((const __m256i *) S0);
	key->part2 = _mm256_loadu_si256((const __m256i *) S1);
}

__m256i avx_xorshift128plus(avx_xorshift128plus_key_t *key) {
	__m256i s1 = key->part1;
	const __m256i s0 = key->part2;
	key->part1 = key->part2;
	s1 = _mm256_xor_si256(key->part2, _mm256_slli_epi64(key->part2, 23));
	key->part2 = _mm256_xor_si256(
			_mm256_xor_si256(_mm256_xor_si256(s1, s0),
					_mm256_srli_epi64(s1, 18)), _mm256_srli_epi64(s0, 5));
	return _mm256_add_epi64(key->part2, s0);
}

void* Thread_calc(void * rank) {
    avx_xorshift128plus_key_t xkey, ykey;

    avx_xorshift128plus_init(123+(uint64_t)rank, 123+(uint64_t)rank, &xkey);
    avx_xorshift128plus_init(456+(uint64_t)rank, 456+(uint64_t)rank, &ykey);

    __m256i numx, numy;
    __m256 xx, yy, mx, my, mask, add, dx, dy, vcnt;
    vcnt = _mm256_setzero_ps();

    long long int i, cnt = 0;
    short j;
    float *ans = (float*) _mm_malloc(8*sizeof(float), 32);

    for(i = 0; i < n; i += 8) {
        numx = avx_xorshift128plus(&xkey);
        xx = _mm256_cvtepi32_ps(numx);
        numy = avx_xorshift128plus(&ykey);
        yy = _mm256_cvtepi32_ps(numy);

		dx = _mm256_div_ps(xx, RND_MAX);
		dy = _mm256_div_ps(yy, RND_MAX);	

		mx = _mm256_mul_ps(dx,dx);
		my = _mm256_mul_ps(dy,dy);

		xx = _mm256_add_ps(mx,my);

		mask = _mm256_cmp_ps(xx, ones, _CMP_LE_OQ);
		add = _mm256_and_ps(mask, ones);
		vcnt = _mm256_add_ps(vcnt, add);
        if(i%1500000000 == 0){
			j = 8;
			_mm256_store_ps(ans, vcnt);
			vcnt = _mm256_setzero_ps();
		
			for( ;j; ){
				--j;
				if(ans[j]) cnt+=ans[j];
			}	
		}
    }
    _mm256_store_ps(ans, vcnt);
    j = 8;
    for( ;j; ){
        --j;
        if(ans[j]) cnt+=ans[j];
    }
    pthread_mutex_lock(&mutex);
    //_mm256_add_pd(number_in_circle, cnt);
    number_in_circle += cnt;
    pthread_mutex_unlock(&mutex);
    pthread_exit(EXIT_SUCCESS);
    // long int my_rank = (long int) rank;
    // double factor;
    // long long int i;
    // long long int my_n = number_of_tosses / thread_count;
    // long long int my_first_i = my_n*my_rank;
    // long long int my_last_i = my_first_i + my_n;
    // long long int my_sum = 0;
    // double x, y, distance_squared;
    // unsigned int seed = time(NULL);
    // for (i = my_first_i; i < my_last_i; i++) {
    //     x = ((double)rand_r(&seed) - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
    //     y = ((double)rand_r(&seed) - (double)(RAND_MAX) / 2) / ((double)(RAND_MAX) / 2);
    //     distance_squared = x * x + y * y;
    //     if (distance_squared <= 1)
    //         my_sum++;
    // }
    // pthread_mutex_lock(&mutex);
    // number_in_circle += my_sum;
    // pthread_mutex_unlock(&mutex);
    // pthread_exit(NULL);
}  /* Thread_sum */

int main(int argc, char *argv[]) {
    long int thread;
    pthread_t * thread_handles;
    // number_of_tosses = 9223372036854775807;
    thread_count = strtol(argv[1], NULL, 10);
    number_of_tosses = strtoll(argv[2], NULL, 10);
    thread_handles = (pthread_t*) malloc (thread_count * sizeof(pthread_t));
    ones = _mm256_set1_ps(1.0f);
    RND_MAX = _mm256_set1_ps(INT32_MAX);
    n = number_of_tosses / thread_count;
    pthread_mutex_init(&mutex, NULL);
    for (thread = 0; thread < thread_count; thread++)  
        pthread_create(&thread_handles[thread], NULL, Thread_calc, (void*)thread);  
    for (thread = 0; thread < thread_count; thread++) 
        pthread_join(thread_handles[thread], NULL);

    
    pi_estimate = 4 * number_in_circle /(( double ) number_of_tosses);
    printf("%.6lf\n", pi_estimate);
    pthread_mutex_destroy(&mutex);
    free(thread_handles);
    return 0;
}