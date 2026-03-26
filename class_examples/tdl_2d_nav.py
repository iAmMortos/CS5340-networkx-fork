
import networkx as nx
from enum import IntEnum

class DirType(IntEnum):
    ORTHOGONAL=1
    CARDINAL=2

map_simple = """
XXXXXXXXXX
X        X
X      E X
X        X
X        X
X S      X
X        X
XXXXXXXXXX
""".strip()

map_wall = """
XXXXXXXXXX
X       EX
X XXXXXX X
X      X X
X      X X
X      X X
XS       X
XXXXXXXXXX
""".strip()

map_long_way = """
XXXXXXXXXX
X       EX
X XXXXXX X
X     SX X
X      X X
X      X X
X        X
XXXXXXXXXX
""".strip()

map_maze = """
XXXXXXXXXX
XE       X
XXXXXXXX X
X    XSX X
X XX   X X
X XXXXXX X
X        X
XXXXXXXXXX
""".strip()

map_no_path = """
XXXXXXXXXX
X   XX  EX
X   XX   X
X   XX   X
X   XX   X
X   XX   X
XS  XX   X
XXXXXXXXXX
""".strip()

def create_graph_from_map(s, dir=DirType.CARDINAL):
    g = nx.grid_2d_graph()
    for y,row in enumerate(s.split('\n')):
        for x,c in enumerate(row):
            print(f'({x}, {y}: {c})')

create_graph_from_map(map_simple)
