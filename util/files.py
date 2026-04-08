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


def load_input(input_file_path: str):
    with open(input_file_path, 'r') as file:
        data = file.readlines()

    rows, cols = map(int, data[0].split())

    flat_board = []

    for row in data[1:]:
        flat_board.extend(map(int, row.split()))

    return BoardTuple(flat_board, rows, cols), rows, cols


def save_solution(solution: list, solution_details: list, solution_file_path: str, solution_details_file_path: str):
    with open(solution_file_path, 'w') as file:
        for i in solution:
            file.write(str(i) + '\n')

    with open(solution_details_file_path, 'w') as file:
        for i in solution_details:
            file.write(str(i) + '\n')
