#include <stdio.h>
#include <stdlib.h>

unsigned int fib(unsigned n) {
    unsigned state = 1;
    unsigned a=0;
    unsigned b=1;
    unsigned int s = b;
    unsigned i;
    while (1) {
        switch (state)
        {
        case 0:
            for (i=2; i<=n; i++) {
                s=a+b;
                a=b;
                b=s;
            }
            state = 3;
            break;
        case 1:
            if (n == 0) {
                return 0;
            }
            state = 0;
            break;
        case 3:
            return s;
        }
    }
}

int main (int argc, char** argv) {
  if (argc < 2) {
    return -1;
  }
  
  unsigned int n = atoi(argv[1]);
  
  printf("result: %u\n", fib(n));
  
  return 0;
}
