from enum import Enum
from typing import override


class Operator(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


class Node:
    def __init__(self: Node, state: tuple, parent: Node = None, depth: int = 0, operator: Operator = "",
                 path: tuple = None):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.operator = operator
        self.path = path

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


def get_neighbors(node: Node):
    neighbors = []

    neighbors.append(node.parent)


def is_goal(node: Node, dbs: tuple) -> bool:
    if node == dbs:
        return True
    return False
