import argparse as ap

parser = ap.ArgumentParser(
    prog='sise_ex1',
    description='Solution for artificial intelligence and expert systems class.',
    epilog='\u00A9 2026 Program made by Filip Szymala & Filip Graczyk',
)


def parse_args():
    parser.add_argument('strategy', type=str, choices=['bfs', 'dfs', 'astr', 'verify_all_results'],
                        help='Search strategy acronym (available: bfs, dfs, astr)', nargs="?", default='bfs')
    parser.add_argument('search_neighbors_strategy', type=str,
                        help='Searching order (e.g. RDUL) for bfs/dfs or heuristics (hamm, manh) for astr', nargs="?",
                        default='RDUL')
    parser.add_argument('input_file', type=str,
                        help='Input file path', nargs="?", default='./resource/4x4_01_00001.txt')
    parser.add_argument('solution_file', type=str,
                        help='Solution file path', nargs="?", default='./out/solution.txt')
    parser.add_argument('solution_details_file', type=str,
                        help='Solution details file path', nargs="?", default='./out/solution_details.txt')

    return parser.parse_args()


def show_args(parsed_args):
    print(parsed_args)