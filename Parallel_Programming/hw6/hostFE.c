#include <stdio.h>
#include <stdlib.h>
#include "hostFE.h"
#include "helper.h"

void hostFE(int filterWidth, float *filter, int imageHeight, int imageWidth,
            float *inputImage, float *outputImage, cl_device_id *device,
            cl_context *context, cl_program *program)
{
    cl_int status;
    int imageSize = imageHeight * imageWidth * sizeof(float);
    int filterSize = filterWidth * filterWidth * sizeof(float);
    int halffilterSize = filterWidth >> 1;

    // Create a command queue
    cl_command_queue command_queue = clCreateCommandQueue(*context, *device, 0, NULL);

    // Create memory buffers on the device for each vector 
    cl_mem input_mem_obj = clCreateBuffer(*context, CL_MEM_USE_HOST_PTR, 
            imageSize, inputImage, NULL);
    cl_mem filter_mem_obj = clCreateBuffer(*context, CL_MEM_USE_HOST_PTR,
            filterSize, filter, NULL);
    cl_mem output_mem_obj = clCreateBuffer(*context, CL_MEM_WRITE_ONLY, 
            imageSize, NULL, NULL);

    // Copy the inputImage and filter to their respective memory buffers
    // clEnqueueWriteBuffer(command_queue, input_mem_obj, CL_TRUE, 0,
    //         imageSize * sizeof(float), inputImage, 0, NULL, NULL);
    // clEnqueueWriteBuffer(command_queue, filter_mem_obj, CL_TRUE, 0, 
    //         filterSize * sizeof(float), filter, 0, NULL, NULL);

    // Create the OpenCL kernel
    cl_kernel kernel = clCreateKernel(*program, "convolution", NULL);

    // Set the arguments of the kernel
    clSetKernelArg(kernel, 0, sizeof(cl_mem), &filter_mem_obj);
    clSetKernelArg(kernel, 1, sizeof(cl_mem), &input_mem_obj);
    clSetKernelArg(kernel, 2, sizeof(cl_mem), &output_mem_obj);
    clSetKernelArg(kernel, 3, sizeof(cl_int), &halffilterSize);
    clSetKernelArg(kernel, 4, sizeof(cl_int), &imageHeight);
    clSetKernelArg(kernel, 5, sizeof(cl_int), &imageWidth);

    // Execute the OpenCL kernel on the list
    int inSize = (imageWidth * imageHeight) >> 2;
    size_t global_item_size = inSize; // Process the entire outputImage
    // size_t local_item_size[2] = {10, 10}; // Divide work items into groups of 16
    clEnqueueNDRangeKernel(command_queue, kernel, 1, NULL, 
            &global_item_size, NULL, 0, NULL, NULL);

    clFinish(command_queue);

    // Read the memory buffer C on the device to the local variable C
    // outputImage = (float*)malloc(sizeof(float)*imageSize);
    clEnqueueReadBuffer(command_queue, output_mem_obj, CL_TRUE, 0, 
            imageSize, outputImage, 0, NULL, NULL);

    // Clean up
    // clFlush(command_queue);
    // clFinish(command_queue);
    // clReleaseKernel(kernel);
    // clReleaseProgram(program);
    // clReleaseMemObject(input_mem_obj);
    // clReleaseMemObject(filter_mem_obj);
    // clReleaseMemObject(output_mem_obj);
    // clReleaseCommandQueue(command_queue);
    // clReleaseContext(context);
}