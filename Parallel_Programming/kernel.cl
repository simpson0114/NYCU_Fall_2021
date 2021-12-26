__kernel void convolution(
    __constant float *filter, __global const float *inputImage, __global float *outputImage,
    int halffilterSize, int imageHeight, int imageWidth) 
{
    const int ix = get_global_id(0);
    const int iy = get_global_id(1);
    

    int fIndex = 0;
    float sum = 0.0;
    for (int k = -halffilterSize; k <= halffilterSize; k++)
    {
        for (int l = -halffilterSize; l <= halffilterSize; l++)
        {
            if(filter[fIndex] == 0) ;
            else {
                if (iy + k >= 0 && iy + k < imageHeight &&
                    ix + l >= 0 && ix + l < imageWidth)
                {
                    sum += inputImage[(iy + k) * imageWidth + ix + l] *
                            filter[fIndex];
                }
            }
            fIndex++;
        }
    }
    outputImage[iy * imageWidth + ix] = sum;
}
