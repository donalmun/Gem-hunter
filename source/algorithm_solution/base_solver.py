from copy import deepcopy
from utils.grid_processing import Grid
from utils.cnf_handle import CNFHandle
from utils.file_processing import write_output_file
import time
from typing import Optional

class SolverBase:
    """Base class for all solvers."""
    def __init__(self, grid: Grid, cnf_agent: CNFHandle, algo_name: str, overwrite: bool):
        self.grid = deepcopy(grid)
        self.cnf_agent = cnf_agent
        self.cnf = cnf_agent.cnf
        self.solution = []
        self.time = 0
        self.algo_name = algo_name
        self.overwrite = overwrite

    def solve(self) -> Optional[list[int]]:
        raise NotImplementedError

    def get_solution(self):
        start = time.time()
        model = self.solve()
        self.time = time.time() - start
        if not model:
            return None
        solution = deepcopy(self.grid.grid)
        for var in model:
            pos = self.cnf_agent.var_to_pos(var)
            if var > 0:
                solution[pos[0]][pos[1]] = 'T'
            else:
                solution[pos[0]][pos[1]] = 'G'
        rows, cols = len(solution), len(solution[0])
        for i in range(rows):
            for j in range(cols):
                if solution[i][j] == '_':
                    solution[i][j] = 'G'
        self.solution = solution
        return solution

    def output_solution(self, filename: str):
        solution = self.get_solution()
        if not solution:
            print(f"{self.algo_name}: No solution")
        write_output_file(solution, filename, self.algo_name, self.overwrite)
