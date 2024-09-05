#include <stdio.h>
#include <stdlib.h>
#include <math.h>
 // For density = 0.05 , q0 = 0.025 , H0 = 67km/s/Mpc

int main (int argc, char **argv)
{
  float A, B , C , D , E, Z=0;
  int SNo=1;
  A = atof(argv[1]);
  B = atof(argv[2]);
  C = atof(argv[3]);

  printf("\n");

  printf("Values of Z and corresponding comoving distances:");
  printf("\n");
  printf("Serial no.\tZ values\tComoving Coordinate\n\n");

  for ( Z =0 ; Z < 5; Z=Z+0.5)
  {
  E = (1)/(1 + Z);
  
  D = A - 0.5*log(E+B+sqrt((E*E+C*E))) + 0.5*log(abs(E +B-sqrt((E*E+C*E))));
  
  printf("%d\t\t%f\t%f\n",SNo++,Z,D);
  }

  printf("\n");
  return 0;
}


/*

A bit more complicated, but also more consistent way is to use 'sscanf()' in one of it's flavors:

Code:

const char* str_int = "777";
const char* str_float = "333.3";
int i;
float f;

if(EOF == sscanf(str_int, "%d", &i))
{
  //error
}

if(EOF == sscanf(str_float, "%f", &f))
{
  //error
}
---------------------
NaN(not a number) error generally occurs if the ouput is indeterminate i.e whose value couldn't be determined such as 0/0.

*/
