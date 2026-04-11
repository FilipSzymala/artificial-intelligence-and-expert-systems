from collections import deque

from util.files import Solution
from util.nodes import is_goal, get_neighbors, Node


# S - start node
# dbs - desired board state
def bfs(S: Node, cols: int, rows: int, search_neighbors_strategy: str, dbs: tuple) -> Solution:
    if is_goal(S, dbs):
        return Solution("", 0, 0, 0, 0)
    # Kolejka stanow otwartych
    Q = deque()
    # Zbior stanow odwiedzonych
    T = set()

    Q.append(S)
    T.add(S)

    visited_states_count = 1
    processed_states_count = 0
    max_depth = 0

    while Q:
        v = Q.popleft()
        processed_states_count += 1
        for i in get_neighbors(v, cols, rows, search_neighbors_strategy):
            if is_goal(i, dbs):
                solution_path = ""
                curr = i
                while curr.parent is not None:
                    solution_path += curr.operator.value
                    curr = curr.parent
                return Solution(solution_path[::-1], len(solution_path), visited_states_count, processed_states_count,
                                max_depth)

            if i not in T:
                if i.depth > max_depth:
                    max_depth = i.depth
                T.add(i)
                Q.append(i)
                visited_states_count += 1

    return Solution(None, -1, visited_states_count, processed_states_count, max_depth)
