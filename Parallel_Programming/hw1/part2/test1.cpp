#include <iostream>
#include <vector>
#include "test.h"
#include "fasttime.h"

using namespace std; 

void test1(float* __restrict a, float* __restrict b, float* __restrict c, int N, int count) {
  __builtin_assume(N == 1024);
  a = (float *)__builtin_assume_aligned(a, 32);
  b = (float *)__builtin_assume_aligned(b, 32);
  c = (float *)__builtin_assume_aligned(c, 32);
  double elapsedf = 0;
  vector<double> result;
  for(int k = 0; k < count; k++) {
    fasttime_t time1 = gettime();
    for (int i=0; i<I; i++) {
      for (int j=0; j<N; j++) {
        c[j] = a[j] + b[j];
      }
    }
    fasttime_t time2 = gettime();
    elapsedf = tdiff(time1, time2);
    if(k == 0)
      result.push_back(elapsedf);
    for(int l = 0; l < k; l++) {
      if(result[l] > elapsedf) {
        result.insert(result.begin() + l, elapsedf);
        cout << elapsedf << " " << l << endl;
        break;
      }
      else if(l == k - 1) {
        result.push_back(elapsedf);
        cout << l << endl;
      }
    }
  }

  if(count % 2 == 1)
    elapsedf = result[count/2];
  else
    elapsedf = (result[count/2 - 1] + result[count/2]) / 2;
  std::cout << "Elapsed execution time of the loop in test1():\n" 
    << elapsedf << "sec (N: " << N << ", I: " << I << ")\n";
}