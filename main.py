from util.parser import *
from util.algoritms import bfs
from util.files import load_input


if __name__ == '__main__':
    args = parse_args()
    show_args(args)

    board, rows, cols = load_input(args.input_file)

    desired_board_state = tuple(range(1, rows * cols)) + (0,)
    # bfs(board, board[0], desired_board_state)
    print(board, rows, cols)
    print(desired_board_state)

    print("Hello World")
