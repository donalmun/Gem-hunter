from copy import deepcopy
from utils.grid_processing import Grid
from utils.cnf_handle import CNFHandle
from typing import Optional
from utils.file_processing import write_output_file
import time
from algorithm_solution.base_solver import SolverBase

class BruteForceSolver(SolverBase):
    """Solve by brute-forcing all binary assignments."""
    def __init__(self, grid, cnf_agent):
        super().__init__(grid, cnf_agent, "Brute force", True)
        self.max_try = 2_000_000

    def solve(self) -> Optional[list[int]]:
        n = self.cnf_agent.var_counter - 1
        for idx, bits in enumerate(range(1 << n)):
            if idx >= self.max_try:
                print("Brute Force Result: Exceeded maximum attempts!")
                return None
            assign = [(bits >> i) & 1 for i in range(n)]
            if self.cnf_agent.is_satisfiable(self.cnf, assign):
                model = [v if assign[v-1] else -v for v in range(1, n+1)]
                print("Brute Force Result: Solution found!")
                # print("Brute force's model:", model)
                return model
        print("Brute Force: No valid solution found.")
        return None
