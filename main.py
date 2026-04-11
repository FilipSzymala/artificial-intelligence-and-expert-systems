from util.algoritms.bfs import bfs
from util.nodes import Node
from util.parser import *
from util.files import load_input, save_solution

if __name__ == '__main__':
    args = parse_args()
    show_args(args)

    board, rows, cols = load_input(args.input_file)

    desired_board_state = tuple(range(1, rows * cols)) + (0,)

    start_node = Node(board.board)
    neighbors_strategy = args.search_neighbors_strategy

    if args.strategy == "bfs":
        solution = bfs(start_node, cols, rows, neighbors_strategy, desired_board_state)

        save_solution(solution.solution, solution.solution_details, "out/solution.txt", "out/solution_details.txt")
    else:
        print("Strategy not implemented yet")