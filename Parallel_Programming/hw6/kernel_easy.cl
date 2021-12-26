__kernel void convolution(
    __constant float *filter, __global const float *inputImage, __global float *outputImage,
    int halffilterSize, int imageHeight, int imageWidth) 
{
    const int ix = get_global_id(0);
    const int iy = get_global_id(1);
    
    int now_x, now_y;
    int fIndex = 0;
    float fNow;
    float sum = 0.0;
    for (int k = -halffilterSize; k <= halffilterSize; k++)
    {
        now_y = iy + k;
        if(now_y >= 0 && now_y < imageHeight) {
            for (int l = -halffilterSize; l <= halffilterSize; l++)
            {
                fNow = filter[fIndex];
                if(fNow == 0) ;
                else 
                {
                    now_x = ix + l;
                    if (now_x >= 0 && now_x < imageWidth)
                    {
                        sum += inputImage[now_y * imageWidth + now_x] *
                                fNow;
                    }
                }
                fIndex++;
            }
        }
    }
    outputImage[iy * imageWidth + ix] = sum;
}
