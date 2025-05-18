from utils.file_processing import read_input_file
from typing import List, Any

class Grid:
    """Grid representation and utility methods for the puzzle."""
    def __init__(self, source: Any):
        self.grid = read_input_file(source) if isinstance(source, str) else source
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0

    def is_valid(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int) -> List[tuple]:
        if not self.is_valid(r, c):
            return []
        return [
            (r + dr, c + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr != 0 or dc != 0) and self.is_valid(r + dr, c + dc)
        ]

    def trap_count(self, r: int, c: int) -> int:
        return sum(1 for nr, nc in self.neighbors(r, c) if self.grid[nr][nc] == 'T')

    def is_correct(self, r: int, c: int) -> bool:
        return self.is_valid(r, c) and self.trap_count(r, c) == self.grid[r][c]

    def is_solved(self) -> bool:
        return all(
            not isinstance(self.grid[i][j], int) or self.is_correct(i, j)
            for i in range(self.rows) for j in range(self.cols)
        )