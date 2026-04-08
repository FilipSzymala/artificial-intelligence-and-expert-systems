def load_input(input_file_path):
    with open(input_file_path, 'r') as file:
        data = file.readlines()

    rows, cols = map(int, data[0].split())

    flat_board = []

    for row in data[1:]:
        flat_board.extend(map(int, row.split()))

    return tuple(flat_board), rows, cols

def save_solution(solution: list, output_file_path):
    with open(output_file_path, 'w') as file:
        # first line from solution list is either length of solution path or -1 if algorithm failed
        file.write(str(solution[0]) + '\n')

        # solution path operators
        if len(solution) > 1:
            file.write(str(solution[1]) + '\n')