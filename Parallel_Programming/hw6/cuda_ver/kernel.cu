__global__ void convKernel(float *inputImage, float *outputImage, float *filter, int halffilterSize, int imageHeight, int imageWidth)