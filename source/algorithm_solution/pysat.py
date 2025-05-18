from copy import deepcopy
from utils.grid_processing import Grid
from utils.cnf_handle import CNFHandle
from pysat.solvers import Solver
from typing import Optional
from utils.file_processing import write_output_file
import time
from algorithm_solution.base_solver import SolverBase

class PysatSolver(SolverBase):
    """Solve using the PySAT library."""
    def __init__(self, grid, cnf_agent):
        super().__init__(grid, cnf_agent, "Pysat", False)

    def solve(self) -> Optional[list[int]]:
        with Solver(bootstrap_with=self.cnf) as solver:
            if solver.solve():
                model = solver.get_model()
                print("Pysat Result: Solution found!")
                # print("Pysat's model:", model)
                return model
            print("Pysat: No valid solution found.")
            return None
