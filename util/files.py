def load_input(input_file_path: str):
    with open(input_file_path, 'r') as file:
        data = file.readlines()

    rows, cols = map(int, data[0].split())

    flat_board = []

    for row in data[1:]:
        flat_board.extend(map(int, row.split()))

    return tuple(flat_board), rows, cols

def save_solution(solution: list, solution_details: list, solution_file_path: str, solution_details_file_path: str):
    with open(solution_file_path, 'w') as file:
        for i in solution:
            file.write(str(i) + '\n')

    with open(solution_details_file_path, 'w') as file:
        for i in solution_details:
            file.write(str(i) + '\n')