2.a:
Register Based ISA
Instructions:
store (register, data)
add (target register, input1, input2)
mov (target register, direct value)
greater than (new_vip, register1, register2)
return (data/register) / print (data/register)
jump (new_vip)
move_init (target register)

5 Instructions (min. 3-bit)
16 Register (min. 4-bit)
input is passed in register 1
0 is return register
All registers are initialized to 0 at the start of the program
ProgramCounter -> vip stored in register 15 in bytes
After every instruction, the program counter is incremented depending on the instruction size

Instruction Encoding:
opcode (1-byte), register (1-byte), (register/data (1-byte))
store: opcode: 0x00, register: target register, data: input data or source register
add: opcode: 0x01, register: target register, data: source register1, source register 2
mov: opcode: 0x02, register: target register, data: direct value
greater than: opcode: 0x03, new_vip: vip to jump to if condition is true, register1, register2
return: opcode: 0x04, register: source register or data to return (maybe just default to register 0)
jump: opcode: 0x05, new_vip: vip to jump to
move_init: opcode: 0x06, register: target register, data: param0 (the input for the program, in this case n)

2.b:
Pseudocode:
move_init r1 // input (n) in register 1
store r2, 0 // store a = 0 in register 2 (Not necessary, all registers are initialized to 0)
mov r3, 1 // b = 1 in register 3
store r4, r3 (or 1 directly) // s = b (always 1) in register 4
if r1 == 0 // if input == 0
    store r0, 0
    return r0 // or directly return 0
mov r5, 2 // init i
if i > n:
    store r0, r4
    return r0 // end program
add r4, r2, r3
store r2, r3
store r3, r4
jmp -6 // jmp to if to loop

VIP  | Bytecode:
0x00 | 0x06 0x01 // move_init r1, input (n)
0x02 | 0x02 0x03 0x01 // mov r3, 1
0x05 | 0x00 0x04 0x02 // store r4, r3 (1)
0x08 | 0x03 0x0E 0x01 0x00 // if r1 > r0 (if n > 0) -> jump to 0x0E
0x0C | 0x04 0x00 // return r0 -> 0
0x0E | 0x02 0x05 0x02 // mov r5, 2
0x11 | 0x03 0x21 0x05 0x01 // if r5 > r1 (if i > n) -> jump to 0x1F (end)
0x15 | 0x01 0x04 0x02 0x03 // add r4, r2, r3 (s = a + b)
0x19 | 0x00 0x02 0x03 // store r2, r3 (a = b)
0x1C | 0x00 0x03 0x04 // store r3, r4 (b = s)
0x1F | 0x05 0x11 // jmp to 0x11 (loop back to if)
0x21 | 0x00 0x00 0x04
0x24 | 0x04 0x00