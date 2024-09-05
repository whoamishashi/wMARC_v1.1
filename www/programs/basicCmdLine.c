#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
        while(argc--)
                printf("%s\n", *argv++);
        return 0;
}

/*

Compiling and running C program from terminal:
'''''''''''''''
dsp@xeon1:~/vsp/shashikant/test_prog/www/cprograms$ gcc ./basicCmdLine.c -o ./basicCmdLine
dsp@xeon1:~/vsp/shashikant/test_prog/www/cprograms$ ./basicCmdLine 12 78 90
./basicCmdLine
12
78
90


Running from Python from python command line terminal:
''''''''''''''''''''
dsp@xeon1:~/vsp/shashikant/test_prog/www/cprograms$ python
Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24) 
[GCC 4.5.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.system("./basicCmdLine 12 78 90")
./basicCmdLine
12
78
90
0

*/
