from collections import deque
from util.nodes import is_goal, get_neighbors

# S - start node
# dbs - desired board state
def bfs(S, cols, rows, search_neighbors_strategy, dbs):
    # kolejka stanow otwartych
    Q = deque()
    # zbior stanow zamknietych
    T = set()
    Q.append(S)

    while Q:
        v = Q.popleft()
        if is_goal(v, dbs):
            return True
        T.add(v)
        for i in get_neighbors(v, cols, rows, search_neighbors_strategy):
            if i not in T and i not in Q:
                Q.append(i)
    return False
