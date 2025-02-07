"""
Advent of Code day 23 part 2
Written by Trevor Ferris
2/5/2025
Notes: Honestly thought that I had the wrong answer since I dont check for if c1Uc2 isn't the longest chain 
(Thinking again that would probably be an extreme edge case where one computer is connected to 27+ computers) but at least it runs fast?
"""

"""PART 2 THOUGHTS
All computers need to be linked to each other 
When you find one computer 
when building the dictionary, build it so that there is only one connection added per entry
put the first alphabetical of the two in the dict

for the each key in the dict compare the intersection of that keys values and the first values values
if that intersection is not empty keep going until it is
record the longest chain
if the length of the difference  of that keys values and the first values values is still greater than the longest chain keep going
otherwise go to the next value in the dict
"""

from typing import Iterator
from time import time

CONNECTIONS_FILENAME = "Aoc23/input.txt"

def load_connections(file_name):
    with open(file_name, "r") as connection_file:
        return [connection.rstrip("\n") for connection in connection_file]

def build_conn_dict(connections):
    conn_dict = {}
    for conn in connections:
        pair = conn.split("-")
        pair.sort()            
        if conn_dict.get(pair[0]):
            conn_dict[pair[0]].append(pair[1])
        else:
            conn_dict[pair[0]] = [pair[1]]
    return {i: sorted(conn_dict[i]) for i in sorted(conn_dict)}

def find_chains(conns: set[str], conn_dict: dict[str: set[str]], long_len: int):    
    """Finds the intersections of a list of connections and the list of connections of the first computer in the list"""
    if not conn_dict.get(conns[0]):
        return [conns[0]]
    shared = [c1 for c1 in conn_dict[conns[0]] if c1 in conns]
    chain = [conns[0]]
    if len(shared) == 1:
        chain.extend(shared)
        return chain
    if len(shared) >= long_len:    
        chain.extend(find_chains(shared, conn_dict, long_len - 1))
    return chain    

def find_connections(conn_dict: dict[str: set[str]]) -> list[str]:
    """Finds the longest chain of computer connections
    
    For each item in the dict check each item in the list of computers it is connected to
    if the intersection of the two lists contains anything add it to a set 
    
    Args:
        conn_dict: Dictionary of {computer: list[connections]}
        
    Returns:
        A list of the longest chain of computer connections"""
    long_chain = []
    for c1, conns in conn_dict.items():
        curr_chain = [c1]
        curr_chain.extend(find_chains(conns, conn_dict, len(long_chain) - 1))
        if len(curr_chain) > len(long_chain):
            long_chain = curr_chain                  
    return long_chain
        
def main():
    start_time = time()
    connections = load_connections(CONNECTIONS_FILENAME)
    conn_dict = build_conn_dict(connections)
    trios = find_connections(conn_dict)
    print(f"Longest chain of connected computers: {",".join(find_connections(conn_dict))}")
    end_time = time()
    print(f"Time: {end_time - start_time}")
    
if __name__ == ("__main__"):
    main()