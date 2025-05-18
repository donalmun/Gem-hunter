# Gem Hunter Game

## Description

Gem Hunter is a logic grid game where players must determine the positions of traps (Trap - 'T') and gems (Gem - 'G') based on numerical hints. Each numbered cell on the grid indicates the number of traps in its 8 adjacent cells. The program's task is to convert this problem into a logical constraint (CNF) and solve it using AI algorithms.

## Installation

Requires Python 3.x and the pysat library.  
Install pysat using pip:
pip install pysat

## Usage

1. Prepare input:  
   - Place input files in the directory testcases/testcase_x/input_x.txt (x is the testcase number).
   - Each input file is a grid consisting of numbers and the character _ (unknown cell).

2. Run the program:  
   - From the root directory, run:
     python source/main.py
   - Results will be written to the corresponding output file in each testcase directory, e.g., testcases/testcase_0/output_0.txt.

3. Results:  
   - Each algorithm will write its solution (if any) to the output file.
   - The running time of each algorithm is recorded in testcases/static_times.txt.

## File Structure

source/
│
├── main.py                      # Main entry point, runs all solvers on testcases
│
├── utils/
│   ├── grid_processing.py       # Defines the Grid class, grid processing functions
│   ├── cnf_handle.py            # Generates CNF from the grid, variable mapping
│   └── file_processing.py       # Reads/writes input/output files, records time
│
├── algorithm_solution/
│   ├── base_agent.py            # Parent class for solvers
│   ├── brute_force.py           # Brute force algorithm
│   ├── backtracking.py          # Backtracking algorithm (DPLL-style)
│   └── pysat.py                 # Solves using the PySAT library
│
└── testcases/
    ├── testcase_0/
    ├── testcase_1/
    └── ...                      # Testcase directories, each containing input_x.txt and output_x.txt

## Algorithms

The project implements 3 algorithms to solve the problem:
- Brute Force: Tries all possible assignments of traps/gems for unknown cells (only for small grids).
- Backtracking: Based on the DPLL algorithm, more efficient than brute force, solves using backtracking and constraints.
- PySAT: Converts the problem to CNF and solves using the modern PySAT library, very fast and efficient for large grids.

