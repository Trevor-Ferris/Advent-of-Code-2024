"""
Advent of Code day 24 part 1
Written by Trevor Ferris
2/6/2024
Notes: check that sick list comprehension
changed to object based wires
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

from time import time
GATES_FILENAME = "Aoc24/input.txt"

class Wire(object):
    def __init__(self, val, from_gate, to_gates):
        self.val = val
        self.from_gate = from_gate
        self.to_gates = to_gates

    def update(self, val, from_gate, to_gates):
        if val != None:
            self.val = val
        if from_gate != None:
            self.from_gate = from_gate
        if to_gates != None:
            self.to_gates = to_gates
            
    def get_val(self):
        return self.val
    
    def read_instr(self, g1, g2, instr):
        match instr:
            case "OR":
                return g1 | g2 
            case "AND":
                return g1 & g2
            case "XOR":
                return g1 ^ g2
        
    def find_val(self, gates):
        if self.val == None:
            if (x := gates[self.from_gate[0]].get_val()) != None and (y := gates[self.from_gate[1]].get_val()) != None:
                self.val = self.read_instr(int(x), int(y), self.from_gate[2])
                return True
            return False
        return True
    
def load_gates(file_name):
    gates = {}
    with open(file_name, "r") as gates_file:
        for line in gates_file:
            if line == ("\n"):
                break
            line = line.rstrip("\n")
            gate, val = line.split(":")
            gates[gate] = Wire(int(val), None, None)
        for line in gates_file:
            line = line.rstrip("\n")
            g1, instr, g2, arrow, g3 = line.split()
            if g1 in gates:
                gates[g1].update(None, None, (g1, g2, instr))
            else:
                gates[g1] = Wire(None, None, (g1, g2, instr))
            if g2 in gates:
                gates[g2].update(None,None, (g1, g2, instr))
            else:
                gates[g2] = Wire(None, None, (g1, g2, instr))
            if g3 in gates:
                gates[g3].update(None, (g1, g2, instr), None)
            else:
                gates[g3] = Wire(None, (g1, g2, instr), None)
    return gates

def dict_gates_to_binary(wires, wire_type):
    return int("".join([str((wires[i].get_val())) for i in reversed(sorted(wires)) if wire_type in i]), 2)
        
def calc_gates(gates): 
    while True:
        comp = True
        for x in gates.values():
            if not x.find_val(gates):
                comp = False
        if comp == True:
            return

def main():
    start_time = time()
    gates = load_gates(GATES_FILENAME)
    calc_gates(gates)
    print(f"Value on z wires {dict_gates_to_binary(gates, "z")}")
    end_time = time()
    print(f"Time: {end_time - start_time}")
if __name__ == ("__main__"):
    main()
