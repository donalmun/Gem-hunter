from pysat.formula import CNF
from itertools import combinations
from utils.grid_processing import Grid
from typing import Dict, Tuple, List

class CNFHandle:
    """Handle CNF generation and variable mapping for the puzzle."""
    def __init__(self):
        self.var_map: Dict[Tuple[int, int], int] = {}
        self.var_counter = 1
        self.cnf: CNF

    def add_var(self, pos: Tuple[int, int]):
        if pos not in self.var_map:
            self.var_map[pos] = self.var_counter
            self.var_counter += 1

    def pos_to_var(self, pos: Tuple[int, int]):
        return self.var_map.get(pos)

    def var_to_pos(self, var: int):
        for pos, v in self.var_map.items():
            if abs(var) == v:
                return pos
        return None

    def map_empty_cells(self, grid: Grid):
        for r in range(grid.rows):
            for c in range(grid.cols):
                if grid.grid[r][c] == '_':
                    self.add_var((r, c))

    def make_clauses(self, vars: List[int], n_traps: int) -> List[List[int]]:
        if len(vars) < n_traps:
            return []
        clauses = [list(comb) for comb in combinations(vars, len(vars) - n_traps + 1)]
        if len(vars) - n_traps > 0:
            clauses += [[-v for v in comb] for comb in combinations(vars, n_traps + 1)]
        return clauses

    def generate_cnf(self, grid: Grid):
        self.map_empty_cells(grid)
        cnf = CNF()
        for i in range(grid.rows):
            for j in range(grid.cols):
                if isinstance(grid.grid[i][j], int):
                    n_traps = grid.grid[i][j]
                    neighbor_vars = []
                    for r, c in grid.neighbors(i, j):
                        if grid.grid[r][c] == '_':  # Only include empty cells
                            var = self.pos_to_var((r, c))
                            if var is not None:  # Double check the variable exists
                                neighbor_vars.append(var)
                    if neighbor_vars:  # Only add clauses if there are valid neighbors
                        cnf.extend(self.make_clauses(neighbor_vars, n_traps))
        cnf.clauses = [list(clause) for clause in set(tuple(sorted(clause)) for clause in cnf.clauses)]
        self.cnf = cnf
        return cnf

    def get_variables(self, cnf: CNF) -> List[int]:
        return list({abs(lit) for clause in cnf.clauses for lit in clause})

    def is_clause_satisfied(self, clause: List[int], assign: List[bool]) -> bool:
        return any((lit > 0 and assign[abs(lit) - 1]) or (lit < 0 and not assign[abs(lit) - 1]) for lit in clause)

    def is_satisfiable(self, cnf: CNF, assign: List[bool]) -> bool:
        return all(self.is_clause_satisfied(clause, assign) for clause in cnf.clauses)