__kernel void convolution(
    __constant float *filter, __global const float *inputImage, __global float4 *outputImage,
    const int halffilterSize, const int imageHeight, const int imageWidth) 
{
    const int gid = get_global_id(0) << 2;
    int now_x = gid % imageWidth;
	int now_y = gid / imageWidth;
    int yy, xx, k, l, wy, pos;
	float4 cal, f;

    int fIndex = 0;
    float4 sum = (float4)0.0;
    for (k = -halffilterSize; k <= halffilterSize; k++)
    {
        yy = now_y + k;
        if(yy >= 0 && yy < imageHeight)
        {
            for (l = -halffilterSize; l <= halffilterSize; l++)
            {
                if(filter[fIndex] == 0) ;
                else {
                    xx = now_x + l;
                    if (xx >= 0 && xx < imageWidth)
                    {
						pos = xx + yy * imageWidth;
						cal = (float4)(inputImage[pos], inputImage[pos+1], inputImage[pos+2], inputImage[pos+3]);

						f = filter[fIndex];
						sum += cal * f;
                    }
                }
                fIndex++;
            }
        }
    }
    outputImage[gid>>2] = sum;
}
