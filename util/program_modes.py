import datetime
import os
import subprocess
import sys

from util.algoritms.bfs import bfs
from util.algoritms.dfs import dfs
from util.algoritms.astr import astr
from util.charts import load_session_data, plot_criterion
from util.nodes import Node
from util.files import load_input, save_solution, save_multiple_solutions


def test_all_mode():
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


def verify_all_mode():
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


def test_number_of_fails_mode():
    fail_count = 0
    success_count = 0
    dfs_count = 0
    bfs_count = 0
    astr_count = 0

    dfs_fails = 0
    bfs_fails = 0
    astr_fails = 0
    for root, dirs, files in os.walk('out/24-04-2026_11-45-37'):
        for file in files:
            if file.endswith('_sol.txt'):
                path = os.path.join(root, file)
                if "dfs" in file:
                    dfs_count += 1
                elif "bfs" in file:
                    bfs_count += 1
                elif "astr" in file:
                    astr_count += 1
                with open(path) as f:
                    if f.readline().strip() == '-1':
                        if "dfs" in file:
                            dfs_fails += 1
                        elif "bfs" in file:
                            bfs_fails += 1
                        elif "astr" in file:
                            astr_fails += 1
                        fail_count += 1
                        print(path)
                    else:
                        success_count += 1
    print(f"===================================================================")
    print(f"{fail_count} solutions were unsolved")
    print(f"{success_count} solutions were solved successfully")
    print(f"===================================================================")
    print(f"{dfs_count} solutions were DFS")
    print(f"{dfs_fails} fails")
    print(f"{bfs_count} solutions were BFS")
    print(f"{bfs_fails} fails")
    print(f"{astr_count} solutions were ASTR")
    print(f"{astr_fails} fails")
    print(f"===================================================================")
    print(f"{fail_count + success_count} was the number of all solutions files")
    print(f"===================================================================")


def generate_charts_mode():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_out_dir = os.path.join(base_dir, "out")

    subdirs = [d for d in os.listdir(base_out_dir)
               if os.path.isdir(os.path.join(base_out_dir, d)) and not d.endswith('_charts')]
    if not subdirs:
        print("No results found in out/ catalogue.")
        return

    # Choose the latest data to generate charts from
    session_name = max(subdirs, key=lambda d: os.path.getmtime(os.path.join(base_out_dir, d)))

    source_path = os.path.join(base_out_dir, session_name)

    charts_dir_name = f"{session_name}_charts"
    charts_path = os.path.join(base_out_dir, charts_dir_name)
    os.makedirs(charts_path, exist_ok=True)

    print(f"Using data from: {source_path}")
    print(f"Destination folder for charts: {charts_path}")

    # load data from catalogue
    df = load_session_data(source_path)

    if df.empty:
        print("No data available to generate charts from.")
        return

    criteria = [
        ('SolLen', 'Długość rozwiązania', 'wyniki_dlugosc.png'),
        ('Visited', 'Liczba stanów odwiedzonych', 'wyniki_odwiedzone.png'),
        ('Processed', 'Liczba stanów przetworzonych', 'wyniki_przetworzone.png'),
        ('MaxDepth', 'Maksymalna osiągnięta głębokość przeszukiwania', 'wyniki_glebokosc.png')
    ]

    for col, title, fname in criteria:
        target_file = os.path.join(charts_path, fname)
        plot_criterion(df, col, title, target_file)

    print(f"Generated charts in: {charts_path}")


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
