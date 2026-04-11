import heapq

from util.files import Solution
from util.nodes import Node, get_neighbors, is_goal


def hamming(state: tuple, dbs: tuple) -> int:
    return sum(1 for i in range(len(state)) if state[i] != 0 and state[i] != dbs[i])

def manhattan(state: tuple, dbs: tuple, cols: int) -> int:
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            goal_idx = dbs.index(state[i])

            curr_row = i // cols
            curr_col = i % cols

            goal_row = goal_idx // cols
            goal_col = goal_idx % cols

            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def astr(S: Node, cols: int, rows: int, search_neighbors_strategy: str, dbs: tuple) -> Solution:
    if is_goal(S, dbs):
        return Solution("", 0, 0, 0, 0)

    open_list = []
    visited = {}

    if search_neighbors_strategy == "manh":
        h = manhattan(S.state, dbs, cols)
    elif search_neighbors_strategy == "hamm":
        h = hamming(S.state, dbs)
    else:
        raise Exception("Invalid search neighbors strategy (valid choices are: hamm, manh)")

    heapq.heappush(open_list, (h, 0, S))
    visited[S.state] = h

    visited_states_count = 1
    processed_states_count = 0
    max_depth = 0

    while open_list:
        f, g, v = heapq.heappop(open_list)
        processed_states_count += 1

        if is_goal(v, dbs):
            solution_path = ""
            curr = v
            while curr.parent is not None:
                solution_path += curr.operator.value
                curr = curr.parent
            return Solution(solution_path[::-1], len(solution_path), visited_states_count, processed_states_count, max_depth)

        for i in get_neighbors(v, cols, rows):
            if search_neighbors_strategy == "manh":
                h = manhattan(i.state, dbs, cols)
            else:
                h = hamming(i.state, dbs)

            new_g = g + 1
            new_f = new_g + h

            if i.state not in visited or new_f < visited[i.state]:
                visited[i.state] = new_f
                if i.depth > max_depth:
                    max_depth = i.depth
                heapq.heappush(open_list, (new_f, new_g, i))
                visited_states_count += 1

    return Solution(None, -1, visited_states_count, processed_states_count, max_depth)