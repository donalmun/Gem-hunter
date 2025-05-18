from pathlib import Path
from typing import List

def read_input_file(filename: str) -> List[List]:
    """Read a grid from a file and return as a 2D list."""
    path = Path(filename)
    if not path.exists():
        print(f"File {filename} does not exist\n")
        return None
    with path.open("r") as f:
        return [[int(cell) if cell.isdigit() else cell for cell in line.strip().split(", ")] for line in f]

def write_output_file(solution: List[List], filename: str, solution_name: str, overwrite: bool):
    """Write a solution grid to a file with a header."""
    mode = "w" if overwrite else "a"
    with open(filename, mode) as f:
        f.write(f"{solution_name}:\n")
        if not solution:
            f.write("No solution\n\n")
            return
        for row in solution:
            f.write(", ".join(str(cell) for cell in row) + "\n")
        f.write("\n")

def output_times(filename: str, times: list[list[float]], sizes: list[tuple[int, int]]):
    """Write timing results and matrix sizes to a file."""
    if not times:
        return
    with open(filename, "w") as f:
        f.write(f"{'Testcase':>10} | {'Size':>10} | {'Brute Force (s)':>20} | {'Backtracking (s)':>20} | {'PySAT (s)':>20}\n")
        for idx, ((bf, bt, ps), (rows, cols)) in enumerate(zip(times, sizes)):
            size_str = f"{rows}x{cols}"
            f.write(f"{idx:10} | {size_str:>10} | {bf:20.6f} | {bt:20.6f} | {ps:20.6f}\n")