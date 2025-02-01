"""
Advent of Code day 17 part 2
Written by Trevor Ferris
1/21/2025
Notes: NUM_BITS is totally a wrong name but I didnt want to do 2**NUM_BITS when I used it
"""

from enum import IntEnum

COMMAND_FILENAME = "Aoc17/input.txt"
NUM_BITS = 8

class Instr(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

def load_commands(file_name):
    with open(file_name, "r") as command_file:
        reg_A = command_file.readline().rstrip("\n")
        reg_A = int(reg_A[reg_A.find(":") + 1:])
        reg_B = command_file.readline().rstrip("\n")
        reg_B = int(reg_B[reg_B.find(":") + 1:])
        reg_C = command_file.readline().rstrip("\n")
        reg_C = int(reg_C[reg_C.find(":") + 1:])
        command_file.readline()
        commands = command_file.readline().rstrip("\n")
        commands = [int(ch) for ch in commands[commands.find(":") + 1:].split(",")]
        return reg_A, reg_B, reg_C, commands

def combo_oper(reg_A, reg_B, reg_C, oper):
    match oper:
        case 0 | 1 | 2 | 3:
            return oper
        case 4:
            return reg_A
        case 5:
            return reg_B
        case 6:
            return reg_C
        case 7:
            print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

def read_instructions(reg_A, reg_B, reg_C, commands):
    pointer = 0
    output = []
    while pointer < len(commands):
        oper = commands[pointer + 1]
        match commands[pointer]:
            case Instr.ADV:
                #Set reg_A to reg_A / combo
                reg_A = reg_A // (2**combo_oper(reg_A, reg_B, reg_C, oper))
            case Instr.BXL:
                #Set reg_B to BXOR literal
                reg_B = reg_B ^ oper
            case Instr.BST:
                #Set reg_B to combo mod 8
                reg_B = combo_oper(reg_A, reg_B, reg_C, oper) % 8
            case Instr.BXC:
                #Set reg_B to reg_B BXOR reg_C
                reg_B = reg_B ^ reg_C
            case Instr.JNZ:
                #If reg_A jump to literal
                if reg_A:
                    pointer = oper - 2
            case Instr.OUT:
                #Appends combo % 8 to output list
                output.append(combo_oper(reg_A, reg_B, reg_C, oper) % 8)
            case Instr.BDV:
                #Set reg_B to reg_A / combo
                reg_B = reg_A // (2**combo_oper(reg_A, reg_B, reg_C, oper))
            case Instr.CDV:
                #Set reg_C to reg_A / combo
                reg_C = reg_A // (2**combo_oper(reg_A, reg_B, reg_C, oper))
        pointer += 2
    return output

def find_next(bit_pos, x, reg_B, reg_C, commands):
    """Checks if the current bit for if the output matches the last bits in the commands"""
    y = NUM_BITS**(bit_pos)
    while True:
        y += NUM_BITS**(bit_pos)
        if read_instructions(x + y, reg_B, reg_C, commands)[bit_pos:] == commands[bit_pos:]:
            break
    return x + y

def find_copy(reg_B, reg_C, commands):
    """Finds the initial value of the A register that results in a copy"""
    bit_pos = len(commands) - 1
    x = NUM_BITS**bit_pos
    while bit_pos >= 0:
        x = find_next(bit_pos, x, reg_B, reg_C, commands)
        bit_pos -= 1
    print (f"Reversed commands:{read_instructions(x, reg_B, reg_C, commands)}")
    return x

def main():
    reg_A, reg_B, reg_C, commands = load_commands(COMMAND_FILENAME)
    print(",".join(str(ch) for ch in read_instructions(reg_A, reg_B, reg_C, commands)))
    print(f"Initial commands: {commands}")
    print(f"reg_A value to copy: {find_copy(reg_B, reg_C, commands)}")   


if __name__ == ("__main__"):
    main()