"""
Advent of Code day 24 part 1
Written by Trevor Ferris
2/6/2024
Notes: check that sick list comprehension
"""

"""            Part 1           
AND OR XOR gates
gates wait for both inputs
gates can be used once per reset
wires can connect to one output but many inputs
from the list of instructions many gates have no values initially

sort the list of instructions by the order that the gates have a result
because each wire can only recieve input from 1 gate
1) the values that you start with cannot have a gate change those values
2) if a wire is being used in a gate it must come after the gate which supplies its value

dict of wires with values, list of gates 
run down list of gates removing any gates which have both values and add the resulting wire to the dict of wires until the list is empty"""

from enum import StrEnum

GATES_FILENAME = "Aoc24/input.txt"

def load_gates(file_name):
    gates = {}
    instructions = []
    with open(file_name, "r") as gates_file:
        for line in gates_file:
            if line == ("\n"):
                break
            line = line.rstrip("\n")
            gate, val = line.split(":")
            gates[gate] = int(val)
        for line in gates_file:
            line = line.rstrip("\n")
            g1, instr, g2, arrow, g3 = line.split()
            instruction = (g1, g2, instr, g3)
            instructions.append(instruction)
    return gates, instructions

def read_instr(g1, g2, instr):
    match instr:
        case "OR":
            return g1 | g2 
        case "AND":
            return g1 & g2
        case "XOR":
            return g1 ^ g2
        
def calc_gates(gates, instructions):
    while instructions:
        for g1, g2, instr, g3 in instructions.copy():
            if g1 in gates and g2 in gates:
                gates[g3] = read_instr(gates[g1], gates[g2], instr)
                instructions.remove((g1, g2, instr, g3))
    return int("".join([str(gates[i]) for i in reversed(sorted(gates)) if "z" in i]), 2)

def main():
    gates, instructions = load_gates(GATES_FILENAME)
    print(f"Result of Z gates: {calc_gates(gates, instructions)}")

if __name__ == ("__main__"):
    main()
