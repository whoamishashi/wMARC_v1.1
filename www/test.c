#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  printf("\nNo. of arguments given: %d \n",argc);
  // printf("%f\n", (return 0));	// does not work because 'return' cannot be a sub-expression (because return is a statement not an expression )
  return -1;
}
