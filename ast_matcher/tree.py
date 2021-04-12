import ast
from collections import deque
from copy import deepcopy
from itertools import chain, product, repeat

from more_itertools import flatten

from .categories.base import BaseNode


class Tree:

    __slots__ = 'ast_node', 'children'

    def __init__(self, ast_node=None, children=None):
        self.children = children or []
        self.ast_node = ast_node


def filter_variation(root):
    todo = deque([root])

    while todo:
        node = todo.popleft()

        node.filter_variation()
        for variation in node.variations:
            todo.extendleft(variation.items)


def walker(start_pattern: BaseNode, tree: ast.AST) -> BaseNode:
    todo = deque([([start_pattern], tree)])

    while todo:
        patterns, node = todo.popleft()

        next_patterns = list(flatten(pattern.last_m for pattern in patterns if pattern.match(node)))
        next_patterns.append(start_pattern)

        todo.extendleft(zip(repeat(next_patterns), ast.iter_child_nodes(node)))

    return start_pattern


def group_children(variation):
    return [
        (ast_node, list(chain.from_iterable((variation_iter(children)))))
        for ast_node, children in variation
    ]


def get_children(variation):
    trees = []

    for ast_node, children in group_children(variation):
        if not children:
            trees.append([Tree(ast_node=ast_node)])
            continue

        trees.append([
            Tree(ast_node=ast_node, children=child)
            for child in children
        ])

    return list(product(*reversed(trees)))


def variation_iter(variations):
    for variation in variations:
        yield list(get_children(variation))


def combine(nodes):
    if not nodes:
        return []

    start, *tail = nodes

    result = [
        [(variation.ast_node, combine(variation.items))]
        for variation in start.variations
    ]

    for node in tail:
        tmp = []
        for variation in node.variations:
            for tree in result:
                for ast_n, _ in tree:
                    if variation.ast_node == ast_n or variation.ast_node.lineno < ast_n.lineno:
                        break
                else:
                    new_tree = tree[:]
                    new_tree.append((variation.ast_node, combine(variation.items)))
                    tmp.append(new_tree)

        if len(tmp) == 0:
            return

        result = tmp

    return result


def flat(node):
    for variation in node.variations:
        items = combine(variation.items)

        if items is None:
            continue

        yield variation.ast_node, items


def make_trees(pattern, py_ast):
    pattern = walker(deepcopy(pattern), py_ast)

    filter_variation(pattern)

    return list(flatten([
        flatten(get_children([variation]))
        for variation in flat(pattern)
    ]))
