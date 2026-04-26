from collections import deque
from util.files import Solution
from util.nodes import is_goal, get_neighbors, Node

def bfs(start_node: Node, cols: int, rows: int, search_neighbors_strategy: str, dbs: tuple) -> Solution:
    if is_goal(start_node, dbs):
        return Solution("", 0, 0, 0, 0)

    open_queue = deque()
    visited = set()

    open_queue.append(start_node)
    visited.add(start_node)

    visited_states_count = 1
    processed_states_count = 0
    max_depth = 0

    while open_queue:
        v = open_queue.popleft()
        processed_states_count += 1
        for i in get_neighbors(v, cols, rows, search_neighbors_strategy):
            visited_states_count += 1

            if i.depth > max_depth:
                max_depth = i.depth

            if i not in visited:
                visited.add(i)
                if is_goal(i, dbs):
                    solution_path = ""
                    curr = i
                    while curr.parent is not None:
                        solution_path += curr.operator.value
                        curr = curr.parent
                    return Solution(solution_path[::-1], len(solution_path), visited_states_count,
                                    processed_states_count, max_depth)
                open_queue.append(i)


    return Solution("", -1, visited_states_count, processed_states_count, max_depth)