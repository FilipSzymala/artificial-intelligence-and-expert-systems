from enum import Enum
from typing import override


class Operators(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


class Node:
    def __init__(self: Node, state: tuple, parent: Node = None, depth: int = 0, operator: Operators = ""):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.operator = operator
        self.zero_idx = state.index(0)

    @override
    def __eq__(self: Node, other: Node | tuple) -> bool:
        if isinstance(other, Node):
            return self.state == other.state
        elif isinstance(other, tuple):
            return self.state == other
        return False

    @override
    def __hash__(self: Node) -> int:
        return hash(self.state)

    @override
    def __lt__(self: Node, other: Node) -> bool:
        return self.depth < other.depth


def get_neighbors(node: Node, cols, rows, search_neighbors_strategy="LRUD"):
    neighbors = []

    zero_idx = node.zero_idx

    for i in search_neighbors_strategy:
        row = zero_idx // cols
        col = zero_idx % cols
        if i == Operators.LEFT.value:
            if col - 1 >= 0:
                temp_state = list(node.state)
                temp_state[zero_idx], temp_state[zero_idx - 1] = temp_state[zero_idx - 1], temp_state[zero_idx]

                new_node = Node(state=tuple(temp_state), parent=node, depth=node.depth + 1, operator=Operators.LEFT)
                neighbors.append(new_node)
        elif i == Operators.RIGHT.value:
            if col + 1 < cols:
                temp_state = list(node.state)
                temp_state[zero_idx], temp_state[zero_idx + 1] = temp_state[zero_idx + 1], temp_state[zero_idx]

                new_node = Node(state=tuple(temp_state), parent=node, depth=node.depth + 1, operator=Operators.RIGHT)
                neighbors.append(new_node)
        elif i == Operators.UP.value:
            if row - 1 >= 0:
                temp_state = list(node.state)
                temp_state[zero_idx], temp_state[zero_idx - cols] = temp_state[zero_idx - cols], temp_state[zero_idx]

                new_node = Node(state=tuple(temp_state), parent=node, depth=node.depth + 1, operator=Operators.UP)
                neighbors.append(new_node)
        elif i == Operators.DOWN.value:
            if row + 1 < rows:
                temp_state = list(node.state)
                temp_state[zero_idx], temp_state[zero_idx + cols] = temp_state[zero_idx + cols], temp_state[zero_idx]

                new_node = Node(state=tuple(temp_state), parent=node, depth=node.depth + 1, operator=Operators.DOWN)
                neighbors.append(new_node)
    return neighbors

def is_goal(node: Node, dbs: tuple) -> bool:
    if node == dbs:
        return True
    return False
