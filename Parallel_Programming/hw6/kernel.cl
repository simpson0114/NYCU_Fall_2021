__kernel void convolution(
    __global const float *filter, __global const float *inputImage, __global float *outputImage,
    int filterWidth, int imageHeight, int imageWidth) 
{
    const int ix = get_global_id(0);
    const int iy = get_global_id(1);
    const int halffilterSize = filterWidth / 2;

    int k;
    for (k = -halffilterSize; k <= halffilterSize; k++)
    {
        for (l = -halffilterSize; l <= halffilterSize; l++)
        {
            if (ix + k >= 0 && ix + k < imageHeight &&
                iy + l >= 0 && iy + l < imageWidth)
            {
                sum += inputImage[(ix + k) * imageWidth + j + l] *
                        filter[(k + halffilterSize) * filterWidth +
                                l + halffilterSize];
            }
        }
    }
    outputImage[ix * imageWidth + iy] = sum;
}
