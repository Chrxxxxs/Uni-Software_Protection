def vm_disassembler(bytecode):
    """Disassembler for the designed VM (Copied and adapted from vm_example.py)"""
    index = 0
    while index < len(bytecode):
        opcode = bytecode[index]

        if opcode == 0:
            print(f"{hex(index)}: store r{bytecode[index + 1]}, r{bytecode[index + 2]}")
            index += 3
        elif opcode == 1:
            print(f"{hex(index)}: add r{bytecode[index + 1]}, r{bytecode[index + 2]}, r{bytecode[index + 3]}")
            index += 4
        elif opcode == 2:
            print(f"{hex(index)}: mov r{bytecode[index + 1]}, {hex(bytecode[index + 2])}")
            index += 3
        elif opcode == 3:
            print(f"{hex(index)}: greater_than {hex(bytecode[index + 1])}, r{bytecode[index + 2]}, r{bytecode[index + 3]}")
            index += 4
        elif opcode == 4:
            print(f"{hex(index)}: return r{bytecode[index + 1]}")
            index += 2
        elif opcode == 5:
            print(f"{hex(index)}: jmp {hex(bytecode[index + 1])}")
            index += 2
        elif opcode == 6:
            print(f"{hex(index)}: move_init r{bytecode[index + 1]}, param0")
            index += 2

bytecode = [
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
]

vm_disassembler(bytecode)