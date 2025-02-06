"""
Advent of Code day 23 part 1
Written by Trevor Ferris
2/5/2025
"""

from typing import Iterator
from time import time

CONNECTIONS_FILENAME = "Aoc23/input.txt"

def load_connections(file_name):
    with open(file_name, "r") as connection_file:
        return [connection.rstrip("\n") for connection in connection_file]

def build_conn_dict(connections):
    conn_dict = {}
    for con in connections:
        c1, c2 = con.split("-")
        if conn_dict.get(c1):
            conn_dict[c1].append(c2)
        else:
            conn_dict[c1] = [c2]
        if conn_dict.get(c2):
            conn_dict[c2].append(c1)
        else:
            conn_dict[c2] = [c1]
    return conn_dict

def find_connections(conn_dict: dict[str: list[str]]) -> set[tuple[str, str, str]]:
    """Finds all 3 computer connections
    
    For each item in the dict check each item in the list of computers it is connected to
    if the intersection of the two lists contains anything add it to a set 
    
    Args:
        conn_dict: Dictionary of {computer: list[connections]}
        
    Returns:
        A set containing each three computer connection in the conn_dict"""
    
    trios = set()
    for c1, conns in conn_dict.items():
        for c2 in conns:
            both_conn = [c3 for c3 in conn_dict[c2] if c3 in conns]
            for c3 in both_conn:                
                l1 = [c1, c2, c3]
                l1.sort()
                trios.add(tuple(l1))                    
    return trios

def find_init_t(trios: set[tuple[int, int, int]]) -> Iterator[int] : 
    for trio in trios:
        if [comp for comp in trio if comp[0] == "t"]:
            yield 1
        
def main():
    start_time = time()
    connections = load_connections(CONNECTIONS_FILENAME)
    conn_dict = build_conn_dict(connections)
    trios = find_connections(conn_dict)
    print(f"Number of connections containing a computer starting with t: {sum(find_init_t(trios))}")
    end_time = time()
    print(f"Time: {end_time - start_time}")
    
if __name__ == ("__main__"):
    main()