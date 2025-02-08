"""
Advent of Code day 24 part 1
Written by Trevor Ferris
2/6/2024
Notes: Idk what im doing, couldn't figure out a good way to find the edge cases(first bit, last carry bit, first carry bit)
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

"""            Part 2
System is trying to binary add x wires with y wires resulting in a z wire equal to x + y
System should be taking in two n bit sets of wires and resulting in n + 1 bits on the z wire
4 pairs of gates are swapped 
record the output wire that is involved in the swap
find which gates on the output are incorrect
(from known answer XOR initial result)
find which gates control those results and swap them
build reverse dict of wires : gates instr
17 bits have the wrong output but only 8 pairs of gates can be swapped
initial wires cant be swapped
normal bitwise add is like 1 XOR 1 s and an AND for the carry?
for a swap to effect multiple z gates it must be effecting multiple outputs
when you switch a gate you are switching an input value on everything that it effects
ie swapping the gate giving the value of bfw will change the value of any gate that relies on bfw 
run through wwdict simulating the change that each gate represents?

NEW PLAN
define each wire type as a part of a bitwise adder
PRIMARY BIT:
two wires that have no from gate and a gate type of AND
PRIMARY CARRY:
two wires that have no from gate and a gate type of XOR
SECONDARY CARRY:
(PRIMARY BIT AND TRUE CARRY BIT - 1)
IF AND and no value 
TRUE CARRY:
SECONDARY CARRY OR PRIMARY CARRY
if gate is OR and no value
RESULT:
PRIMARY BIT XOR TRUE CARRY BIT - 1
if XOR and no value
"""

from enum import StrEnum
from time import time

GATES_FILENAME = "Aoc24/input.txt"
EDGE_CASES = ["z00", "z45", "bdj"]

class G(StrEnum):
    PRIMARY = "PRIMARY"
    S_CARRY = "S_CARRY"
    P_CARRY = "P_CARRY"
    T_CARRY = "T_CARRY"
    RESULT = "RESULT"

class W(StrEnum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    PROCESS = "PROCESS"

class Wire(object):
    """Defines a wire from the input file and contains links to the gates the wire is touching"""
    def __init__(self, name: str, val: int):
        self.name = name
        self.val = val
        self.f_gate = None
        self.t_gate = []    
        self.type = None

    def update_type(self):
        if self.f_gate:
            if self.t_gate:
                self.type = W.PROCESS
            else:
                self.type = W.OUTPUT
        else:
            self.type = W.INPUT

    def set_f_gate(self, f_gate):
        self.f_gate = f_gate
        self.update_type()

    def set_t_gate(self, t_gate):
        self.t_gate.append(t_gate)
        self.update_type()

    def set_val(self, val: int):
        self.val = val

    def get_name(self) -> str:
        return self.name
    
    def get_val(self) -> int:
        return self.val
    
    def get_type(self) -> W:
        return self.type

    def get_f_gate(self):
        return self.f_gate
    
    def get_t_gate(self):
        return self.t_gate

class Gate(object):
    """Defines a gate from the file and contains links to the wires it effects/is effected by"""
    def __init__(self, type):
        self.type = type
        self.cat = None
        self.val = None
        self.i_w1 = None
        self.i_w2 = None
        self.o_w = None

    def link_gates(self, w1: Wire, w2: Wire, w3: Wire):
        """Links the gate to the wires
        Args:
            i_w1: First input wire
            i_w2: Second input wire
            o_w: Output wire
        """
        self.i_w1 = w1
        self.i_w2 = w2
        self.o_w = w3

    def find_cat(self):
        """Sets the category of the wire as defined by its gate type and input wires
        
        PRIMARY CARRY: two input wires and a gate type of AND
        SECONDARY CARRY: no input wires and a gate type of AND
        PRIMARY BIT:two input wires and a gate type of XOR
        RESULT: no input wires and a gate type of XOR
        TRUE CARRY: OR gate type
        """        
        match self.type:
            case "AND":
                if self.i_w1.get_type() == W.INPUT and self.i_w2.get_type() == W.INPUT:
                    self.cat = G.P_CARRY
                else:
                    self.cat = G.S_CARRY
            case "XOR":
                if self.i_w1.get_type() == W.INPUT and self.i_w2.get_type() == W.INPUT:
                    self.cat = G.PRIMARY
                else:
                    self.cat = G.RESULT
            case "OR":
                self.cat = G.T_CARRY 

    def check_correct(self):  
        """Checks if the output wire of the gate is leading to the correct gates for its category
        
        PRIMARY: Feeds result and true carry
        PRIMARY CARRY: Feeds secondary carry
        SECONDARY CARRY: Feeds true carry
        TRUE CARRY: Feeds secondary carry and result
        RESULT: Feeds output wire
        """
        match self.cat:
            case G.RESULT: 
                if self.o_w.get_type() != W.OUTPUT:
                    return self.o_w.get_name()
            case G.T_CARRY:
                gates = self.o_w.get_t_gate()
                if not gates:
                    return self.o_w.get_name()
                for gate in gates:
                    if gate.get_cat() not in (G.S_CARRY, G.RESULT):
                        return self.o_w.get_name()
            case G.S_CARRY:
                gates = self.o_w.get_t_gate()
                if not gates:
                    return self.o_w.get_name()
                for gate in self.o_w.get_t_gate():
                    if gate.get_cat() not in (G.T_CARRY):
                        return self.o_w.get_name()
            case G.P_CARRY:
                gates = self.o_w.get_t_gate()
                if not gates:
                    return self.o_w.get_name()
                for gate in self.o_w.get_t_gate():
                    if gate.get_cat() not in (G.T_CARRY):
                        return self.o_w.get_name()
            case G.PRIMARY:
                gates = self.o_w.get_t_gate() 
                if not gates:
                    return self.o_w.get_name()
                for gate in self.o_w.get_t_gate():
                    if gate.get_cat() not in (G.S_CARRY, G.RESULT):
                        return self.o_w.get_name()
                                                       
    def find_val(self):
        """Sets the values of the gate and the output wire to the value given by its gate type"""
        if self.i_w1.get_val() != None and self.i_w2.get_val() != None:
            match self.type:
                case "AND":
                    self.val = self.i_w1.get_val() & self.i_w2.get_val()
                    self.o_w.set_val(self.val)
                case "XOR":
                    self.val = self.i_w1.get_val() ^ self.i_w2.get_val()
                    self.o_w.set_val(self.val)
                case "OR":
                    self.val = self.i_w1.get_val() | self.i_w2.get_val()
                    self.o_w.set_val(self.val)

    def get_cat(self):
        return self.cat
    
    def has_val(self):
        return self.val != None
    
def load_gates(file_name):
    wires = {}
    gates = []
    with open(file_name, "r") as wires_file:
        for line in wires_file:
            if line == ("\n"):
                break
            line = line.rstrip("\n")
            wire, val = line.split(":")
            wires[wire] = Wire(wire, int(val))
        for line in wires_file:
            line = line.rstrip("\n")
            w1, instr, w2, arrow, w3 = line.split()
            for w in (w1, w2, w3):
                if w not in wires:
                    wires[w] = Wire(w, None)
            new_gate = Gate(instr)
            new_gate.link_gates(wires[w1], wires[w2], wires[w3])
            wires[w1].set_t_gate(new_gate)
            wires[w2].set_t_gate(new_gate)    
            wires[w3].set_f_gate(new_gate)
            gates.append(new_gate)
    for gate in gates:
        gate.find_cat()
    return wires, gates

def wires_to_binary(wires, wire_type):
    """Converts the value on the wires of a given type to decimal"""
    return int("".join([str((wires[i].get_val())) for i in reversed(sorted(wires)) if wire_type in i]), 2)

def find_bad_gates(gates):
    """Yields a list of gates which have incorrect values"""
    for gate in gates:
        if (x := gate.check_correct()): 
            if x not in EDGE_CASES:    
                yield x

def calc_wires(gates): 
    """Finds the values of each wire"""
    while True:
        comp = True
        for x in gates:
            if not x.has_val():
                x.find_val()
                comp = False
        if comp == True:
            return
 
def main():
    start_time = time()
    wires, gates = load_gates(GATES_FILENAME)
    calc_wires(gates)
    print(wires_to_binary(wires, "z"))
    print(",".join(sorted(list(find_bad_gates(gates)))))
    end_time = time()
    print(f"Time: {end_time - start_time}")
if __name__ == ("__main__"):
    main()
