#include <stdio.h> 
#include <stdlib.h>
#include <time.h> 
 
int main ()
{
	/* Simple "srand()" seed: just use "time()" */
	unsigned int iseed = (unsigned int)time(NULL);
	srand (iseed);
	/* Now generate 5 pseudo-random numbers */
	int i;
	for (i=0; i<5; i++)
	    printf ("rand[%d]= %u\n", i, rand ());
	return 0;
}


// rand() accepts no arguments, and returns a single value.
// srand() is more portable than randomize() which may be windows-specific.
// The randomize() or srand() initialize the random number generator, rand(), with a value.
