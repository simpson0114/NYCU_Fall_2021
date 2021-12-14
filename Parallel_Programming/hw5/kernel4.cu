#include <cuda.h>
#include <stdio.h>
#include <stdlib.h>

/*inline void CUDA_ERROR_CHECK(const cudaError_t &err){
	if(err != cudaSuccess){
		fprintf(stderr, "CUDA error: %s\n", cudaGetErrorString(err));
		exit(EXIT_FAILURE);
	}
}*/

__device__ int mandel(float c_re, float c_im, int maxIteration)
{
	float z_re = c_re, z_im = c_im;
    float new_re, new_im;

	int i = 0;
	while(i < maxIteration)
	{
		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;

		if (z_re * z_re + z_im * z_im > 4.f)
		    break;

		new_re = z_re * z_re - z_im * z_im;
		new_im = 2.f * z_re * z_im;
		z_re = c_re + new_re;
		z_im = c_im + new_im;

		++i;
	}

	return i;
}


__global__ void mandelKernel(float lowerX, float lowerY, float stepX, float stepY, int *d_res, int resX, int resY, int maxIterations){
    // To avoid error caused by the floating number, use the following pseudo code
    //
    // float x = lowerX + thisX * stepX;
    // float y = lowerY + thisY * stepY;

    int now_x = blockIdx.x * blockDim.x + threadIdx.x;
	int now_y = blockIdx.y * blockDim.y + threadIdx.y;

	if(now_x < resX || now_y < resY) {
		float x = lowerX + now_x * stepX;
		float y = lowerY + now_y * stepY;
		int idx = now_y * resX + now_x;
		d_res[idx] = mandel(x, y, maxIterations);
	}
}

// Host front-end function that allocates the memory and launches the GPU kernel
void hostFE (float upperX, float upperY, float lowerX, float lowerY, int* img, int resX, int resY, int maxIterations)
{
	// float stepX = (upperX - lowerX) / resX;
	// float stepY = (upperY - lowerY) / resY;

	// int blocksX = ;
	// int blocksY = ;

	dim3 block(16, 16);
	dim3 grid((int) ceil(resX/16.0), (int) ceil(resY/16.0));

	int *d_res;
	int size = resX * resY * sizeof(int);

	cudaMalloc((void**)&d_res, size);
	//int *h = (int*)malloc(size);
	
	mandelKernel <<< grid, block >>> (lowerX, lowerY, (upperX - lowerX) / resX, (upperY - lowerY) / resY, d_res, resX, resY, maxIterations);
	
	cudaMemcpy(img, d_res, size, cudaMemcpyDeviceToHost);
	//memcpy(img, h, size);

	//free(h);
	cudaFree(d_res);
}