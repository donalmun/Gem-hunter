from copy import deepcopy
from utils.grid_processing import Grid
from utils.cnf_handle import CNFHandle
from typing import Optional, List, Dict, Tuple
from utils.file_processing import write_output_file
import time
from algorithm_solution.base_solver import SolverBase
from collections import defaultdict

class BacktrackingSolver(SolverBase):
    """Solve using optimized backtracking (DPLL-style)."""
    def __init__(self, grid, cnf_agent):
        super().__init__(grid, cnf_agent, "Backtracking", False)
        self.max_try = 2_000_000

    def solve(self):
        res = self._dpll(self.cnf_agent.cnf)
        if res is None:
            print("Backtracking Result: Exceeded maximum attempts!")
            return None
        sat, assign = res
        if not sat:
            print("Backtracking: No valid solution found.")
            return None
        # Sử dụng model giống với PySAT: biến gán True (trap) = số dương, False (gem) = số âm
        model = []
        for v in self.cnf_agent.get_variables(self.cnf):
            if v in assign and assign[v]:
                model.append(v)  # Trap
            else:
                model.append(-v)  # Gem
        print("Backtracking Result: Solution found!")
        return model

    def _find_unit_clauses(self, cnf: List[List[int]], assign: Dict[int, bool]) -> List[int]:
        """Tìm các unit clause (mệnh đề chỉ có 1 literal chưa gán) và trả về literal cần gán."""
        unit_literals = []
        for clause in cnf:
            # Lọc ra các literal chưa được gán giá trị
            unassigned = [lit for lit in clause if abs(lit) not in assign]
            # Nếu chỉ còn 1 literal chưa gán, đó là unit clause
            if len(unassigned) == 1:
                unit_literals.append(unassigned[0])
        return unit_literals

    def _unit_propagation(self, cnf: List[List[int]], assign: Dict[int, bool]) -> Tuple[List[List[int]], Dict[int, bool], bool]:
        """Áp dụng unit propagation cho CNF."""
        while True:
            unit_literals = self._find_unit_clauses(cnf, assign)
            if not unit_literals:
                break
                
            for lit in unit_literals:
                var = abs(lit)
                # Gán giá trị sao cho literal này True
                assign[var] = lit > 0
                
                # Lọc bỏ các mệnh đề đã thỏa mãn (chứa lit)
                cnf = [c for c in cnf if lit not in c]
                
                # Loại bỏ -lit từ các mệnh đề còn lại (đã False)
                cnf = [[l for l in c if l != -lit] for c in cnf]
                
                # Kiểm tra xem có mệnh đề rỗng không (mâu thuẫn)
                if any(len(c) == 0 for c in cnf):
                    return [], assign, False
        
        return cnf, assign, True

    def _dpll(self, cnf: List[List[int]], assign: Dict[int, bool] = None, depth: int = 0) -> Optional[Tuple[bool, Dict[int, bool]]]:
        """Thuật toán DPLL với unit propagation."""
        if assign is None:
            assign = {}
        if depth > self.max_try:
            return None
            
        # Unit propagation
        cnf, assign, status = self._unit_propagation(cnf, assign)
        if not status:  # Nếu phát hiện mâu thuẫn
            return False, {}
        if not cnf:  # Nếu tất cả mệnh đề đều thỏa mãn
            return True, assign
            
        # Chọn biến tiếp theo (lấy biến đầu tiên tìm thấy)
        unassigned = next((abs(lit) for clause in cnf for lit in clause if abs(lit) not in assign), None)
        if unassigned is None:
            return True, assign
            
        # Thử gán True và False
        for val in (True, False):
            assign2 = assign.copy()
            assign2[unassigned] = val
            
            # Đơn giản hóa CNF dựa trên phép gán
            new_cnf = []
            for clause in cnf:
                # Nếu clause chứa literal đúng, bỏ qua clause này (đã thỏa mãn)
                if (unassigned if val else -unassigned) in clause:
                    continue
                # Loại bỏ literal sai khỏi clause
                new_clause = [lit for lit in clause if lit != (-unassigned if val else unassigned)]
                new_cnf.append(new_clause)
                
            # Nếu tạo ra mệnh đề rỗng, phép gán này không thỏa mãn
            if any(len(c) == 0 for c in new_cnf):
                continue
                
            res = self._dpll(new_cnf, assign2, depth + 1)
            if res is not None:
                sat, final_assign = res
                if sat:
                    return True, final_assign
                    
        return False, {}
