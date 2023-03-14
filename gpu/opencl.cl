__kernel void multiply(int n, int m, int p,
__global int *a, __global int *b, __global int *c)
{
  int t = get_global_id(0);
  int row_a = t/n;
  int coln_b = t%p;

  for (int i=0; i <m; i++) {
   c[t] += a[row_a*m+i] * b[i*p+coln_b];
  }
}