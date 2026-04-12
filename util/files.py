import datetime
from os import makedirs, path
from typing import override


class BoardTuple:
    def __init__(self, board: list, rows: int, cols: int):
        self.board = tuple(board)
        self.rows = rows
        self.cols = cols
        self.zero_idx = self.board.index(0)

    @override
    def __str__(self):
        result = ""
        for i in range(len(self.board)):
            if self.board[i] / 10 >= 1:
                result += f"{self.board[i]} "
            else:
                result += f"{self.board[i]}  "

            if (i + 1) % self.cols == 0:
                result += "\n"
        return result

class Solution:
    def __init__(self, solution_path, solution_length, visited_count, processed_count, max_depth):
        self.solution_path = solution_path
        self.solution_length = solution_length
        self.visited_count = visited_count
        self.processed_count = processed_count
        self.max_depth = max_depth
        self.solution = [solution_length, solution_path]
        self.solution_details = [solution_length, visited_count, processed_count, max_depth]

def load_input(input_file_path: str):
    with open(input_file_path, 'r') as file:
        data = file.readlines()

    rows, cols = map(int, data[0].split())

    flat_board = []

    for row in data[1:]:
        flat_board.extend(map(int, row.split()))

    return BoardTuple(flat_board, rows, cols), rows, cols

def save_solution(solution: list, solution_details: list, solution_output_path: str = "", solution_details_output_path: str = ""):
    if solution_output_path and solution_details_output_path:
        solution_file_path = solution_output_path
        solution_details_file_path = solution_details_output_path
        makedirs(path.dirname(solution_file_path), exist_ok=True)
        makedirs(path.dirname(solution_details_file_path), exist_ok=True)
    else:
        session_dir = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        dir_path = f"out/{session_dir}"
        makedirs(dir_path, exist_ok=True)
        solution_file_path = f"{dir_path}/solution_sol.txt"
        solution_details_file_path = f"{dir_path}/solution_sol_details.txt"

    with open(solution_file_path, 'w') as file:
        for item in solution:
            file.write(str(item) + '\n')

    with open(solution_details_file_path, 'w') as file:
        for item in solution_details:
            file.write(str(item) + '\n')

def save_multiple_solutions(solutions: list, solutions_details: list, file_name: str, session_dir: str):
    bfs_dirs = [
        'bfs_RDUL', 'bfs_RDLU', 'bfs_DRUL', 'bfs_DRLU', 'bfs_LUDR', 'bfs_LURD', 'bfs_ULDR', 'bfs_ULRD'
    ]
    dfs_dirs = [
        'dfs_RDUL', 'dfs_RDLU', 'dfs_DRUL', 'dfs_DRLU', 'dfs_LUDR', 'dfs_LURD', 'dfs_ULDR', 'dfs_ULRD'
    ]
    astr_dirs = [
        'astr_hamm', 'astr_manh'
    ]
    solution_dirs = [*bfs_dirs, *dfs_dirs, *astr_dirs]

    for idx, solution_dir in enumerate(solution_dirs):
        dir_path = f"out/{session_dir}/{solution_dir}"
        makedirs(dir_path, exist_ok=True)

        sol_file = f"{dir_path}/{file_name}_sol.txt"
        sol_details_file = f"{dir_path}/{file_name}_sol_details.txt"

        with open(sol_file, 'w') as file:
            for item in solutions[idx]:
                file.write(str(item) + '\n')

        with open(sol_details_file, 'w') as file:
            for item in solutions_details[idx]:
                file.write(str(item) + '\n')
