#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

// Function to be virtualized
unsigned int fib(unsigned n)
{
    unsigned a = 0;
    unsigned b = 1;
    unsigned int s = b;
    unsigned i;

    if (n == 0)
    {
        return 0;
    }

    for (i = 2; i <= n; i++)
    {
        s = a + b;
        a = b;
        b = s;
    }
    return s;
}

unsigned int vm_execute(unsigned char *bytecode, unsigned int param0)
{
    // init vm state
    uint32_t vip = 0;      // virtual instruction pointer
    int32_t reg[16] = {0}; // 16 registers
    uint8_t opcode;
    uint8_t target_reg, input1, input2, new_vip;
    int32_t return_value = 0;

    // fetch-decode-execute loop
    while (1)
    {
        opcode = bytecode[vip];
        if (opcode == 0x00) // store instruction
        {
            target_reg = bytecode[vip + 1];
            input1 = bytecode[vip + 2];
            reg[target_reg] = reg[input1];
            vip += 3;
        }
        else if (opcode == 0x01) // add instruction
        {
            target_reg = bytecode[vip + 1];
            input1 = bytecode[vip + 2];
            input2 = bytecode[vip + 3];
            reg[target_reg] = reg[input1] + reg[input2];
            vip += 4;
        }
        else if (opcode == 0x02) // move immediate instruction
        {
            target_reg = bytecode[vip + 1];
            input1 = bytecode[vip + 2];
            reg[target_reg] = input1;
            vip += 3;
        }
        else if (opcode == 0x03) // greater than instruction
        {
            new_vip = bytecode[vip + 1];
            input1 = bytecode[vip + 2];
            input2 = bytecode[vip + 3];
            if (reg[input1] > reg[input2])
            {
                vip = new_vip;
            }
            else
            {
                vip += 4;
            }
        }
        else if (opcode == 0x04) // return instruction
        {
            target_reg = bytecode[vip + 1];
            return_value = reg[target_reg];
            break; // exit the loop and return the value
        }
        else if (opcode == 0x05) // jump instruction
        {
            new_vip = bytecode[vip + 1];
            vip = new_vip;
        }
        else if (opcode == 0x06) // move_init instruction
        {
            target_reg = bytecode[vip + 1];
            reg[target_reg] = param0;
            vip += 2;
        }
        else
        {
            // invalid opcode, halt execution
            printf("Invalid opcode: 0x%02x\n", opcode);
            exit(-1);
        }
    }
    return return_value;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        return -1;
    }

    unsigned int n = atoi(argv[1]);

    unsigned char bytecode[] = {
        0x06, 0x01,
        0x02, 0x03, 0x01,
        0x00, 0x04, 0x02,
        0x03, 0x0E, 0x01, 0x00,
        0x04, 0x00,
        0x02, 0x05, 0x02,
        0x03, 0x21, 0x05, 0x01,
        0x01, 0x04, 0x02, 0x03,
        0x00, 0x02, 0x03,
        0x00, 0x03, 0x04,
        0x05, 0x11,
        0x00, 0x00, 0x04,
        0x04, 0x00,
    };

    printf("vm result: %u\n", vm_execute(bytecode, n));

    printf("result: %u\n", fib(n));

    return 0;
}
