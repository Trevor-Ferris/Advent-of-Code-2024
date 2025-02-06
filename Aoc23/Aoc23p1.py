"""
Advent of Code day 23 part 1
Written by Trevor Ferris
2/5/2025
"""

CONNECTIONS_FILENAME = "Aoc23/inputtest.txt"

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

def main():
    connections = load_connections(CONNECTIONS_FILENAME)
    conn_dict = build_conn_dict(connections)
    for key, val in conn_dict.items():
        print(key, ":", val)
    print(connections)

if __name__ == ("__main__"):
    main()