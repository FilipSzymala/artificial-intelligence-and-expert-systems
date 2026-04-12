import datetime
import os
import subprocess
import sys

from util.algoritms.bfs import bfs
from util.algoritms.dfs import dfs
from util.algoritms.astr import astr
from util.nodes import Node
from util.files import load_input, save_solution, save_multiple_solutions

def test_all_mode(args):
    DEPTH_LIMIT = 20

    resource_files = [f"resource/{f}" for f in os.listdir("resource")]

    total = len(resource_files)
    start_time = datetime.datetime.now()
    session_dir = start_time.strftime('%d-%m-%Y_%H-%M-%S')

    for processed, current_file in enumerate(resource_files, start=1):
        board, rows, cols = load_input(current_file)
        file_name = current_file.split("/")[-1].split(".")[0]
        desired_board_state = tuple(range(1, rows * cols)) + (0,)
        start_node = Node(board.board)

        solutions = []
        solutions_details = []

        bfs_dfs_variants = ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']
        astr_heuristics = ['hamm', 'manh']

        percent = (processed / total) * 100

        width = 100
        print("=" * width)
        print(f"  Now processing: {current_file}  ".center(width, "="))
        print(f"  {processed}/{total} ({percent:.1f}%) - {file_name}  ".center(width, "="))
        print("=" * width)

        for order in bfs_dfs_variants:
            res = bfs(start_node, cols, rows, order, desired_board_state)
            solutions.append(res.solution)
            solutions_details.append(res.solution_details)
            print(f"Processing bfs_{order} done")

        for order in bfs_dfs_variants:
            res = dfs(start_node, DEPTH_LIMIT, cols, rows, order, desired_board_state)
            solutions.append(res.solution)
            solutions_details.append(res.solution_details)
            print(f"Processing dfs_{order} done")

        for heur in astr_heuristics:
            res = astr(start_node, cols, rows, heur, desired_board_state)
            solutions.append(res.solution)
            solutions_details.append(res.solution_details)
            print(f"Processing astr_{heur} done")

        print(f"Saving results to files")
        save_multiple_solutions(solutions, solutions_details, file_name, session_dir)
        print(f"Results saved")

    endtime = datetime.datetime.now()
    elapsed = endtime - start_time
    print(f"Script processing ended after: {elapsed}")


def verify_all_mode(args):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(base_dir)
    out_dir = os.path.join(base_dir, 'out')

    if sys.platform == 'win32':
        script_path = os.path.join(out_dir, 'verify_results.ps1')
        cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path]
    else:
        script_path = os.path.join(out_dir, 'verify_results.sh')
        cmd = ['bash', script_path]

    subprocess.run(cmd, cwd=out_dir)

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
