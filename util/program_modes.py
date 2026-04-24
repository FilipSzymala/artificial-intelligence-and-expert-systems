from util.algoritms.bfs import bfs
from util.algoritms.dfs import dfs
from util.algoritms.astr import astr
from util.nodes import Node
from util.files import load_input, save_solution

def default_mode(args):
    board, rows, cols = load_input(args.input_file)
    desired_board_state = tuple(range(1, rows * cols)) + (0,)
    start_node = Node(board.board)
    neighbors_strategy = args.search_neighbors_strategy
    DEPTH_LIMIT = 20

    if args.strategy == "bfs":
        solution = bfs(start_node, cols, rows, neighbors_strategy, desired_board_state)
        save_solution(solution.solution, solution.solution_details, args.solution_file, args.solution_details_file)
    elif args.strategy == "dfs":
        solution = dfs(start_node, DEPTH_LIMIT, cols, rows, neighbors_strategy, desired_board_state)
        save_solution(solution.solution, solution.solution_details, args.solution_file, args.solution_details_file)
    elif args.strategy == "astr":
        solution = astr(start_node, cols, rows, neighbors_strategy, desired_board_state)
        save_solution(solution.solution, solution.solution_details, args.solution_file, args.solution_details_file)
    else:
        print("Strategy doesn't exist.")
