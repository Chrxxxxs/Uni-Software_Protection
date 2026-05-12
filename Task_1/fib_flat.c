#include <stdio.h>
#include <stdlib.h>

unsigned int fib(unsigned n) {
    // Putting initialization of variables in a switch statement generates a warning/error depending on the c-version
    unsigned state = 1;
    unsigned a=0;
    unsigned b=1;
    unsigned int s = b;
    unsigned i;
    // The while loop simulates the dispatcher loop of a state machine, and the switch statement simulates the state transitions.
    while (1) {
        switch (state)
        {
        case 0: // Original loop to calculate Fibonacci numbers
            for (i=2; i<=n; i++) {
                s=a+b;
                a=b;
                b=s;
            }
            state = 2;
            break;
        case 1: // Entry block: check if n == 0 (I hope this was meant by "the entry block of the original function should also be protected")
            if (n == 0) {
                state = 3;
            } else {
                state = 0;
            }
            break;
        case 2: // Return state after the loop
            return s;
        case 3: // Return state for n == 0
            return 0;
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
