from collections import deque
from util.nodes import is_goal

def bfs(G, S, dbs):
    Q = deque()
    T = set()
    Q.append(S)

    while Q:
        v = Q.popleft()
        if is_goal(v, dbs):
            return True
        T.add(v)
        for i in G.neighbors(v):
            if i not in T and i not in Q:
                Q.append(i)
    return False
