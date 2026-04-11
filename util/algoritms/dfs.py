from collections import deque

from util.files import Solution
from util.nodes import Node, is_goal, get_neighbors


def dfs(S: Node, depth_limit, cols: int, rows: int, search_neighbors_strategy: str, dbs: tuple) -> Solution:
    if is_goal(S, dbs):
        return Solution("", 0, 0, 0, 0)

    stack = []
    visited = set()

    stack.append(S)
    visited.add(S)

    visited_states_count = 1
    processed_states_count = 0
    max_depth = 0

    while stack:
        v = stack.pop()
        processed_states_count += 1

        for i in reversed(get_neighbors(v, cols, rows, search_neighbors_strategy)):
            if is_goal(i, dbs):
                solution_path = ""
                curr = i
                while curr.parent is not None:
                    solution_path += curr.operator.value
                    curr = curr.parent
                return Solution(solution_path[::-1], len(solution_path), visited_states_count, processed_states_count, max_depth)

            if i not in visited and i.depth <= depth_limit:
                if i.depth > max_depth:
                    max_depth = i.depth
                visited.add(i)
                stack.append(i)
                visited_states_count += 1

    return Solution(None, -1, visited_states_count, processed_states_count, max_depth)