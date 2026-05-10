Register Based ISA
Instructions:
load (register) -> might be not necessary, conditions / stores could use register directly
store (register, data)
add (target register, input1, input2)
if (condition)
loop/while (condition) -> could be just a jump after if
return (data/register) / print (data/register)

5 Instructions (3-bit)
16 Register (4-bit)
0 is return register
ProgramCounter (?)

Pseudocode:
store r1, input // input (n) in register 1
store r2, 0 // store a = 0 in register 2
store r3, 1 // b = 1 in register 3
store r4, r3 (or 1 directly) // s = b (always 1) in register 4
if r1 == 0 // if input == 0
    store r0, 0
    return r0 // or directly return 0
store r5, 2 // init i
if i > n:
    store r0, r4
    return r0 // end program
add r4, r2, r3
store r2, r3
store r3, r4
jmp -6 // jmp to if to loop

