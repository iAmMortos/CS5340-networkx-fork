"""
Example: Solving a Sudoku Grid Using NetworkX's Sudoku Graph Structure

This example demonstrates how to use NetworkX's sudoku_graph to model and solve
a Sudoku puzzle using graph coloring concepts and backtracking constraint satisfaction.
"""

import networkx as nx
from typing import List, Set, Dict, Tuple, Optional


def node_to_position(node: int, n: int = 3) -> Tuple[int, int]:
    """Convert a node index to (row, col) position in the grid."""
    grid_size = n * n
    row = node // grid_size
    col = node % grid_size
    return row, col


def position_to_node(row: int, col: int, n: int = 3) -> int:
    """Convert (row, col) position to node index."""
    grid_size = n * n
    return row * grid_size + col


def get_box(row: int, col: int, n: int = 3) -> int:
    """Get the box number for a given position."""
    return (row // n) * n + (col // n)


class SudokuSolver:
    """
    Sudoku solver using NetworkX graph structure.
    
    The solver models Sudoku constraints as a graph coloring problem where:
    - Vertices represent cells in the Sudoku grid
    - Edges connect cells in the same row, column, or box (constraints)
    - Colors (1-9) represent the allowed values
    """
    
    def __init__(self, puzzle: List[List[int]], n: int = 3):
        """
        Initialize the solver with a Sudoku puzzle.
        
        Args:
            puzzle: 9x9 grid (or n²xn² for n-Sudoku) with 0 representing empty cells
            n: Order of the Sudoku (default 3 for standard 9x9)
        """
        self.n = n
        self.grid_size = n * n
        self.graph = nx.sudoku_graph(n)
        self.puzzle = [row[:] for row in puzzle]  # Copy the puzzle
        
        # Maintain possible values for each cell
        self.possibilities: Dict[int, Set[int]] = {}
        self._initialize_possibilities()
    
    def _initialize_possibilities(self):
        """Initialize the set of possible values for each cell."""
        all_values = set(range(1, self.grid_size + 1))
        
        for node in self.graph.nodes():
            row, col = node_to_position(node, self.n)
            
            if self.puzzle[row][col] != 0:
                # Cell is given, no possibilities
                self.possibilities[node] = {self.puzzle[row][col]}
            else:
                # Start with all values
                self.possibilities[node] = all_values.copy()
        
        # Constrain based on neighbors
        for node in self.graph.nodes():
            row, col = node_to_position(node, self.n)
            if self.puzzle[row][col] == 0:
                for neighbor in self.graph.neighbors(node):
                    n_row, n_col = node_to_position(neighbor, self.n)
                    if self.puzzle[n_row][n_col] != 0:
                        value = self.puzzle[n_row][n_col]
                        self.possibilities[node].discard(value)
    
    def propagate_constraints(self) -> bool:
        """
        Apply constraint propagation to reduce possibilities.
        
        Returns:
            False if a contradiction is found, True otherwise.
        """
        changed = True
        while changed:
            changed = False
            
            # Naked singles: cells with only one possibility
            for node in self.graph.nodes():
                row, col = node_to_position(node, self.n)
                if self.puzzle[row][col] == 0 and len(self.possibilities[node]) == 1:
                    value = list(self.possibilities[node])[0]
                    self.puzzle[row][col] = value
                    
                    # Remove this value from neighbors
                    for neighbor in self.graph.neighbors(node):
                        if value in self.possibilities[neighbor]:
                            self.possibilities[neighbor].discard(value)
                            changed = True
                    
                    if not changed:
                        changed = True
                
                # Empty possibilities = contradiction
                if len(self.possibilities[node]) == 0 and self.puzzle[row][col] == 0:
                    return False
        
        return True
    
    def solve(self) -> bool:
        """
        Solve the Sudoku puzzle using backtracking with constraint propagation.
        
        Returns:
            True if puzzle is solved, False if unsolvable.
        """
        # Apply constraint propagation
        if not self.propagate_constraints():
            return False
        
        # Find empty cell with minimum possibilities (MRV heuristic)
        min_node = None
        min_count = self.grid_size + 1
        
        for node in self.graph.nodes():
            row, col = node_to_position(node, self.n)
            if self.puzzle[row][col] == 0:
                count = len(self.possibilities[node])
                if count == 0:
                    return False  # No solution possible
                if count < min_count:
                    min_count = count
                    min_node = node
        
        if min_node is None:
            return True  # All cells filled, puzzle solved!
        
        row, col = node_to_position(min_node, self.n)
        
        # Try each possibility
        for value in sorted(list(self.possibilities[min_node])):
            # Save state
            old_puzzle = [r[:] for r in self.puzzle]
            old_possibilities = {n: s.copy() for n, s in self.possibilities.items()}
            
            # Try this value
            self.puzzle[row][col] = value
            self.possibilities[min_node] = {value}
            
            # Update neighbors
            for neighbor in self.graph.neighbors(min_node):
                self.possibilities[neighbor].discard(value)
            
            # Recurse
            if self.solve():
                return True
            
            # Backtrack
            self.puzzle = old_puzzle
            self.possibilities = old_possibilities
        
        return False
    
    def display(self):
        """Display the Sudoku grid in a readable format."""
        print("\n" + "+" + "-" * (self.grid_size * 2 + self.n - 1) + "+")
        
        for row in range(self.grid_size):
            if row % self.n == 0 and row != 0:
                print("+" + "-" * (self.grid_size * 2 + self.n - 1) + "+")
            
            line = "|"
            for col in range(self.grid_size):
                line += f" {self.puzzle[row][col]}"
                if (col + 1) % self.n == 0:
                    line += "|"
            print(line)
        
        print("+" + "-" * (self.grid_size * 2 + self.n - 1) + "+\n")


def main():
    """Example: Solve a standard 9x9 Sudoku puzzle."""
    
    # Example puzzle (0 represents empty cells)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    
    print("=" * 50)
    print("Sudoku Solver Using NetworkX")
    print("=" * 50)
    
    print("\nInitial Puzzle:")
    solver = SudokuSolver(puzzle)
    solver.display()
    
    print("Solving...")
    if solver.solve():
        print("Solution Found!")
        solver.display()
    else:
        print("No solution exists for this puzzle.")
    
    # Demonstrate graph structure
    print("\nGraph Information:")
    G = nx.sudoku_graph(3)
    print(f"Sudoku Graph Nodes: {G.number_of_nodes()}")
    print(f"Sudoku Graph Edges: {G.number_of_edges()}")
    print(f"Graph Degree (regular): {G.degree(0)}")
    print(f"Chromatic Number (theoretical): 9")
    print(f"Clique Number (theoretical): 9")
    
    # Show neighbors of center cell (node 40 is the center cell)
    center_node = 40
    neighbors = sorted(list(G.neighbors(center_node)))
    print(f"\nNeighbors of center cell (node {center_node}):")
    print(f"Count: {len(neighbors)}")
    print(f"Nodes: {neighbors}")


if __name__ == "__main__":
    main()
