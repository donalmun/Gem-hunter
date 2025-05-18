import os
from utils.grid_processing import Grid
from utils.cnf_handle import CNFHandle
from utils.file_processing import output_times
from algorithm_solution.brute_force import BruteForceSolver
from algorithm_solution.backtracking import BacktrackingSolver
from algorithm_solution.pysat import PysatSolver

def run_all_solvers(testcases_dir="testcases", time_file="result_times.txt"):
    """Run all solvers for each input in each testcase subfolder and write output in the same subfolder."""
    all_times = []
    all_sizes = []
    solvers = [BruteForceSolver, BacktrackingSolver, PysatSolver]
    solver_names = ["Brute force", "Backtracking", "Pysat"]
    testcase_folders = sorted([
        os.path.join(testcases_dir, d) for d in os.listdir(testcases_dir)
        if os.path.isdir(os.path.join(testcases_dir, d))
    ])
    for testcase_dir in testcase_folders:
        input_files = [f for f in os.listdir(testcase_dir) if f.startswith("input_") and f.endswith(".txt")]
        if not input_files:
            continue
        inp_file = input_files[0]
        inp_path = os.path.join(testcase_dir, inp_file)
        out_file = inp_file.replace("input_", "output_")
        out_path = os.path.join(testcase_dir, out_file)
        print(f"{inp_path}:")
        grid = Grid(inp_path)
        print(f"Grid size: {grid.rows}x{grid.cols}")
        cnf = CNFHandle(); cnf.generate_cnf(grid)
        results = []
        times = []
        for Solver, name in zip(solvers, solver_names):
            print(f"Running {name}...")
            try:
                solver = Solver(grid, cnf)
                solver.output_solution(out_path)
                results.append(solver)
                times.append(solver.time)
                print(f"{name} completed in {solver.time:.2f} seconds.")
            except KeyboardInterrupt:
                print(f"{name} was interrupted. Skipping to next solver.")
                times.append(0)
                continue
        for solver, name in zip(results, solver_names):
            if solver.solution:
                check = Grid(solver.solution)
                print(f"{name}: ", "satisfiable" if check.is_solved() else "not satisfiable")
        all_times.append(times)
        all_sizes.append((grid.rows, grid.cols))
        print()
    output_times(os.path.join(testcases_dir, time_file), all_times, all_sizes)

if __name__ == "__main__":
    run_all_solvers()